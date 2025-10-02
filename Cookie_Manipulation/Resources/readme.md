# Cookie Manipulation - Admin Bypass

## Vulnerability:
The website uses a cookie value to check if the user is an admin.
The cookie value is stored as an MD5 hash and validated client-side.

## Weakness:
- Cookie value can be manipulated on the client side
- MD5 hash can be easily reversed or regenerated
- No proper server-side validation
- Trusting client-side data for authorization

## Exploitation:
1. Current cookie value: 68934a3e9455fa72420237eb05902327
2. Cracked hash using CrackStation: "false"
3. Generated MD5 hash of "true": b326b5062b2f0e69046810717534cb09
4. Modified cookie value with new hash
5. Refreshed page and obtained flag

## How to Fix:
- Never store sensitive information in cookies
- Implement server-side session management
- Use signed cookies to prevent tampering
- Use secure token systems like JWT
- Always validate admin status on the server side
- Use HttpOnly and Secure flags for cookies