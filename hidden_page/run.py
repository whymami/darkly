#!/usr/bin/env python3
import asyncio
import hashlib
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import aiohttp
import aiofiles

unique_files: dict[str, str] = {}
visited_pages: set[str] = set()
MAX_CONCURRENT_REQUESTS = 10

class LinkExtractor(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.sub_links: list[str] = []
        self.readme_list: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        for attr, val in attrs:
            if attr == "href" and val:
                if val.startswith("README"):
                    self.readme_list.append(urljoin(self.base, val))
                elif not val.startswith(".."):
                    self.sub_links.append(urljoin(self.base, val))

async def fetch_text(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore) -> str | None:
    try:
        async with sem:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    print(f"⚠️ {url} returned status {resp.status}")
                    return None
    except Exception as e:
        print(f"✖ Error fetching {url}: {e}")
        return None

async def process_readme(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore, lock: asyncio.Lock):
    text = await fetch_text(session, url, sem)
    if text is None:
        return
    digest = hashlib.md5(text.encode()).hexdigest()
    async with lock:
        if digest in unique_files:
            print(f"⚠️ Skipped (duplicate): {url} -> {unique_files[digest]}")
            return
        unique_files[digest] = url
        print(f"✅ New README: {url}")
    try:
        async with aiofiles.open("collected_readmes_async.txt", "a+", encoding="utf-8") as f:
            await f.write("\n" + "=" * 60 + "\n")
            await f.write(f"URL: {url}\n")
            await f.write(f"MD5: {digest}\n")
            await f.write("=" * 60 + "\n")
            await f.write(text + "\n")
    except Exception as e:
        print(f"✖ Error writing to file ({url}): {e}")

async def explore_and_collect(start_base: str = "http://104.238.21.89/", start_dirs: list[str] = None):
    if start_dirs is None:
        start_dirs = [".hidden/"]
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    lock = asyncio.Lock()
    async with aiohttp.ClientSession() as session:
        queue: asyncio.Queue[str] = asyncio.Queue()
        for d in start_dirs:
            queue.put_nowait(urljoin(start_base, d))
        tasks = []
        async def worker():
            while True:
                try:
                    page_url = await asyncio.wait_for(queue.get(), timeout=3.0)
                except asyncio.TimeoutError:
                    return
                normalized = page_url.rstrip("/")
                if normalized in visited_pages:
                    queue.task_done()
                    continue
                visited_pages.add(normalized)
                print(f"🔎 Scanning: {page_url}")
                body = await fetch_text(session, page_url, sem)
                if body is None:
                    queue.task_done()
                    continue
                parser = LinkExtractor(page_url)
                try:
                    parser.feed(body)
                except Exception as e:
                    print(f"⚠️ Parser error ({page_url}): {e}")
                for readme_url in parser.readme_list:
                    tasks.append(asyncio.create_task(process_readme(session, readme_url, sem, lock)))
                for link in parser.sub_links:
                    base_domain = urlparse(start_base).netloc
                    link_domain = urlparse(link).netloc or base_domain
                    if link_domain == base_domain:
                        queue.put_nowait(link)
                queue.task_done()
        workers = [asyncio.create_task(worker()) for _ in range(6)]
        await asyncio.gather(*workers)
        if tasks:
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(explore_and_collect())
    except KeyboardInterrupt:
        print("Cancelled.")
    print("\n" + "=" * 31)
    print(f"Summary: {len(unique_files)} unique README files found")
    print("=" * 31)
    for md5sum, url in unique_files.items():
        print(f"{md5sum}: {url}")
