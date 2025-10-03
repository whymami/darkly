# Cross-Site Scripting (XSS) - Media SRC Reflection

## Vulnerability:
A Cross-Site Scripting (XSS) vulnerability exists where user-controlled input in the `src` parameter of the `page=media` endpoint is reflected and interpreted by the browser. This allows injection of arbitrary script content that executes in victims' browsers.

## Weakness:
- User input is not properly validated or sanitized before being included in HTML output.
- Output is not correctly encoded for the context where the input is placed.
- Content-type and source filtering for `src` values is absent or insufficient (e.g., `data:` URIs accepted).
- No Content Security Policy (CSP) restricting inline scripts or untrusted sources.
- No input whitelisting or strict parsing for allowed media sources.

## Exploitation:
1. The `src` parameter can contain a `data:` URI that includes HTML/JS which the browser will parse and execute.
2. Example discovered payloads:
   - Reflected script injection (plain):  
     `http://104.238.21.89/index.php?page=media&src=data:text/html,<script>alert("xss")</script>`
   - Base64-encoded variant:  
     `http://104.238.21.89/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgieHNzIik8L3NjcmlwdD4=`
3. Visiting these URLs causes the injected script to run in the context of the site, demonstrating arbitrary JavaScript execution in the victim’s browser.
4. Depending on the context and user session, an attacker could exfiltrate session cookies, perform actions as the victim, or deliver further payloads.

> Note: Payloads above are provided as sanitized PoC for authorized testing only.

## Flag / Evidence:
- Evidence: JavaScript alert observed when the above URLs are loaded (proof of concept).  
- No challenge flag associated with this finding (N/A).  
- For internal reporting, include a screenshot of the alert and request/response logs in the `Resources` folder — do not publish screenshots that include sensitive user data.

## PoC (sanitized requests / URIs):
```text
# Plain data URI (reflected)
GET /index.php?page=media&src=data:text/html,<script>alert("xss")</script>

# Base64-encoded data URI (reflected)
GET /index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgieHNzIik8L3NjcmlwdD4=

Reproduce only in authorized environments. Capture request/response and a screenshot of the executed payload for evidence.
```

Impact:

Execution of arbitrary JavaScript in users’ browsers (session theft, CSRF amplification, UI redressing, malware delivery).

If administrative users are targeted, full account takeover of admin functionalities may be possible.

Phishing or persistence attacks via stored XSS variants (if the injection can be stored) are possible.

How to Fix:

Disallow data: URIs for src unless explicitly required and strictly validated. Prefer only whitelisted schemes (e.g., https:) and vetted hostnames.

Validate and normalize input: accept only expected formats (e.g., file identifiers, sanitized filenames, or signed resource tokens) — never raw HTML or arbitrary URIs from user input.

Contextual output encoding: encode user-supplied values appropriately for the HTML attribute context (src attribute), using proper framework/template escaping functions.

Avoid inserting untrusted HTML into pages. If embedding user content is required, render it safely (e.g., via server-side sanitization libraries that strip scripts) or present it in a sandboxed iframe with restricted sandbox attributes.

Implement a strict Content Security Policy (CSP) that disallows inline scripts ('unsafe-inline') and restricts script/src to trusted origins.

Set secure headers: X-Content-Type-Options: nosniff, X-XSS-Protection: 0 (or rely on CSP instead), and appropriate Referrer-Policy.

Use HTTP-only, Secure cookies and rotate sessions after sensitive actions to reduce impact of stolen cookies.

Perform input whitelisting for media parameters (e.g., only allow references to server-hosted media via an ID mapped to a safe path).


