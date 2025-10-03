# Local File Inclusion / Path Traversal - Arbitrary File Read

## Vulnerability:
A Local File Inclusion (LFI) / path traversal vulnerability exists in the `page` parameter that allows an attacker to traverse the filesystem and read arbitrary files. The parameter accepts input such as `../../.../etc/passwd`, which the application includes or returns without proper validation.

## Weakness:
- User-controlled file path is used directly by the application (no canonicalization or validation).
- No allowlist of safe resource identifiers (application accepts raw paths/filenames).
- Missing input normalization and path traversal mitigation (e.g., removal of `../` segments).
- Lack of privilege separation for the web process or over-permissive file read permissions.
- No logging/alerting for suspicious file access patterns.

## Exploitation (non-actionable / summary):
1. The `page` parameter was manipulated to request system files:
   - Example payload used: `?page=../../../../../../../../../../../etc/passwd`
2. The server responded by returning the contents of `/etc/passwd` (proof of arbitrary file read).
3. Successful file read demonstrates the ability to exfiltrate sensitive files (password file entries, configuration files, SSH keys if readable) which can lead to user enumeration or further compromise.
4. **Do not include step-by-step exploitation commands or automate attacks in public reports**; keep PoC sanitized for authorized testing only.

## Evidence / Flag:
- Evidence: Request to `/index.php?page=../../../../../../../../../../../etc/passwd` returned contents of `/etc/passwd`.  
- For the `flag` file: place any discovered challenge flag into the `flag` file in the challenge folder (do not include plaintext credentials in shared reports).
- Capture and keep sanitized request/response logs and a screenshot for internal reporting.

## PoC (sanitized):
GET /index.php?page=../../../../../../../../../../../etc/passwd
- Reproduce only in authorized/CTF environments. Collect and store evidence privately.

## Impact:
- Disclosure of system files (e.g., `/etc/passwd`, application config files) which may reveal usernames, configuration secrets, or paths to other sensitive files.
- If readable files include credentials, private keys, or configuration containing secrets, an attacker can escalate to remote code execution or lateral movement.
- High severity when sensitive files (database credentials, PRIVATE KEYS, config files) are accessible.

## How to Fix:
- Never allow raw file paths from user input. Instead:
  - Use an allowlist of permitted resource identifiers (IDs or filenames mapped server-side to safe paths).
  - Canonicalize and validate paths: resolve the requested path and reject if it escapes the intended base directory.
  - Remove or disallow path traversal sequences (`..`, `../`, percent-encoded equivalents) before any file access.
- Run the web application with least-privilege filesystem permissions; the web user should only have read access to intended files.
- Store sensitive files (private keys, configs with secrets) outside the web-accessible directory and with restrictive permissions.
- If the application must serve files, map user-supplied identifiers to server-side paths using a safe lookup table rather than direct concatenation.
- Log and alert on suspicious file-access patterns (repeated `../`, long path manipulations, attempts to read system files).
- Conduct code review and static analysis focusing on file inclusion/IO paths.
