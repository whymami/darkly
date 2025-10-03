# Stored XSS (Cross-Site Scripting)

## Vulnerability:
The website does not properly sanitize user input before storing
and displaying it. This allows attackers to inject malicious JavaScript
code that will be executed in other users' browsers.

## Weaknesses Found:
1. No input validation on user-submitted content
2. No output encoding/escaping when displaying stored data
3. User input is stored in database without sanitization
4. HTML/JavaScript execution is allowed in input fields
5. No Content Security Policy (CSP) implemented

## Exploitation Steps:
1. Identified input field vulnerable to XSS (comment, feedback, or message form)
2. Tested basic XSS payload: <script>alert('XSS')</script>
3. Used SVG-based payload to bypass filters: <svg/onload=alert('XSS')>
4. Injected payload into the input field
5. Payload was stored in the database
6. Upon page reload or when other users view the content, JavaScript executes
7. Retrieved flag after successful XSS execution

## Attack Vectors:
- Cookie stealing: document.cookie
- Session hijacking
- Keylogging
- Phishing attacks
- Malware distribution
- Defacement

## OWASP Classification:
- A03:2021 - Injection
- A07:2021 - Identification and Authentication Failures

## How to Fix:
1. Input Validation:
   - Whitelist allowed characters
   - Reject dangerous patterns
   - Validate data type and format

2. Output Encoding:
   - HTML entity encoding for HTML context
   - JavaScript encoding for JS context
   - URL encoding for URL parameters
   - Use templating engines with auto-escaping

3. Content Security Policy (CSP):
   - Implement strict CSP headers
   - Disable inline JavaScript
   - Whitelist trusted sources

4. Security Headers:
   - X-XSS-Protection: 1; mode=block
   - X-Content-Type-Options: nosniff

5. Use Security Libraries:
   - DOMPurify for HTML sanitization
   - OWASP Java Encoder
   - Framework-specific sanitization functions

6. HTTPOnly Cookies:
   - Prevent JavaScript access to session cookies
