# Insecure Client‑Side Controls — Password Recovery Manipulation

## Vulnerability:
The password recovery functionality relies on client-side HTML values (e.g., an email address or user identifier rendered in the page) that can be modified by an attacker in the browser. By editing the HTML/form field before submission, it was possible to trigger a recovery flow for a different account and obtain the challenge flag.

## Weakness:
- Trusting client-side values for authorization-sensitive operations.
- No server‑side verification that the recovery request corresponds to the authenticated or intended user.
- Lack of server-side checks such as email confirmation, token verification, or ownership validation.
- Insufficient rate-limiting or verification on password recovery endpoints.

## Exploitation:
1. Open the password recovery page in a browser.
2. Inspect the HTML/form field (e.g., `email` or hidden input that contains target email/identifier).
3. Modify the value in the DOM (change the email to the target account) and submit the recovery request.
4. The server processed the injected value and returned the flag (or the recovery response included the flag).
5. Evidence: successful response contained the flag. (Store full request/response in internal `Resources` for evidence; do not share sensitive artifacts publicly.)

> Note: steps above are a high-level PoC for authorized testing and reporting. Do not include raw credentials or full exploit payloads in public reports.

## Flag / Evidence:
- Place the extracted flag into the `flag` file inside the challenge folder (or record it here as `FLAG{REDACTED}` if you must redact for sharing).
- Keep sanitized request/response logs and any screenshots in `Resources/` for private review.

## How to Fix:
- Never trust client-supplied values for authorization or account selection. Always validate on the server side that the requester is authorized to perform the recovery for the specified account.
- Require out-of-band verification for recovery actions:
  - Send a one-time, time-limited recovery token to the registered email address and require that token to complete recovery.
  - Do not expose secret or sensitive information in recovery responses.
- Use per-request, single-use tokens and verify them server-side before revealing any account-specific data.
- Implement strict rate-limiting and monitoring on recovery endpoints to detect abuse.
- Log password recovery attempts with sufficient detail for investigation (but never log plaintext credentials or token values).
- Consider adding CAPTCHAs on abuse-prone flows and MFA for high-privilege accounts.
