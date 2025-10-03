# HTTP Header Spoofing - User-Agent & Referer Validation Bypass

## Vulnerability:
The website implements security checks based on HTTP headers
(User-Agent and Referer) which can be easily spoofed by attackers.
This is a client-side validation that provides no real security.

## Weaknesses Found:
1. Security logic depends on client-controlled HTTP headers
2. User-Agent validation can be bypassed
3. Referer header validation is insufficient
4. No server-side authentication mechanism
5. Trusting client-provided data for access control

## Exploitation Steps:
1. Identified that the page checks User-Agent header
2. Modified User-Agent to: ft_bornToSec
3. Identified that the page checks Referer header
4. Modified Referer to: https://www.nsa.gov/
5. Combined both headers in a single request
6. Accessed restricted page with hash: b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f
7. Retrieved flag from response

## OWASP Classification:
- A01:2021 - Broken Access Control
- A04:2021 - Insecure Design
- A07:2021 - Identification and Authentication Failures

## How to Fix:
- Never rely on HTTP headers for security decisions
- User-Agent and Referer can be easily spoofed
- Implement proper authentication and authorization
- Use session-based or token-based authentication
- Validate user identity on the server side
- HTTP headers should only be used for logging/analytics
- Implement proper access control lists (ACLs)
- Use OAuth2 or similar secure authentication methods