# Unrestricted File Upload — Content‑Type (MIME) Spoofing

## Vulnerability:
The file upload endpoint accepts user-supplied files and trusts the `Content-Type` header (or filename extension) to determine the file type. By spoofing the MIME type, an attacker can upload a PHP file disguised as an image and have it stored/served by the application, potentially leading to remote code execution if the file is accessible/executable on the server.

## Weakness:
- Server-side validation relies on the `Content-Type` header or filename extension, which can be tampered with by an attacker.
- No server-side inspection of file magic bytes / signature (e.g., using `finfo`).
- Uploads are stored in a web-accessible location where uploaded files can be executed.
- No execution restrictions in the upload directory (PHP execution enabled).
- Insufficient logging, rate-limiting, or post-upload scanning for malicious content.

## Exploitation:
1. The attacker uploads a `.php` file using the normal upload form (appears as an image upload flow).
2. The upload request is intercepted (e.g., with a proxy) and forwarded to a repeater/editor.
3. The `Content-Type` header in the request is modified to `image/jpeg` (or another allowed MIME type) before replaying the request.
4. The server accepts the upload because it trusts the declared MIME type and stores the file in a location that can be accessed/executed.
5. If the uploaded file is accessible via the web and the server executes PHP in that location, the attacker may achieve command execution or upload a web shell.

> Evidence: describe captured request/response and server-stored file path in internal report; do not include actual malicious payloads in shared reports.

## How to Fix:
- Never trust client-provided `Content-Type` or file extensions. Validate file types server-side by checking file signatures (magic bytes) with reliable libraries (e.g., `finfo` in PHP).
- Store uploaded files outside the webroot or in directories configured to prevent script execution.
- Rename uploaded files and assign safe extensions (e.g., store as `.dat` or serve via a proxy that sets `Content-Disposition`), rather than preserving user-supplied names.
- Enforce an allowlist of acceptable file types and limit file sizes.
- Re-encode image uploads server-side (e.g., load and re-save via an image library) to strip embedded code.
- Apply strict permissions on upload directories and disable execution (e.g., with webserver config: `php_admin_flag engine off` for that location or deny `*.php`).
- Scan uploads for malware and suspicious content (AV or heuristic scanning) and log upload events for auditing.
- Implement rate-limiting and authentication for upload functionality; alert on anomalous upload patterns.

## PoC / Notes (sanitized):
- Upload flow: use the application’s normal image upload form.
- Interception: capture the HTTP multipart upload request in a proxy (for reporting/investigation only).
- Modify header: change `Content-Type` for the file part to `image/jpeg` before replaying.
- Do not include or share working web shells, raw PHP payloads, or direct commands in public reports—store any sensitive artifacts (uploaded file, request/response) only in the private `Resources` folder of the CTF report.
