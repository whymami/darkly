# Sensitive File Exposure & Weak Credentials

## Vulnerability:
The website exposes sensitive files through robots.txt and uses
weak password hashing with easily crackable credentials.

## Weaknesses Found:
1. robots.txt reveals hidden directories
2. Plaintext username in exposed file
3. MD5 hashed password (weak hashing algorithm)
4. Weak password that exists in common password databases
5. No rate limiting on admin login

## Exploitation Steps:
1. Discovered robots.txt file containing disallowed paths
2. Found /whatever directory listed in robots.txt
3. Accessed the file containing credentials:
   - Username: root
   - Password hash (MD5): 437394baff5aa33daa618be47b75cb49
4. Cracked hash using CrackStation: qwerty123@
5. Logged into /admin with credentials root:qwerty123@
6. Retrieved flag from admin panel

## OWASP Classification:
- A01:2021 - Broken Access Control
- A02:2021 - Cryptographic Failures
- A05:2021 - Security Misconfiguration

## How to Fix:
- Never expose sensitive files in robots.txt
- Use robots.txt only for SEO, not security
- Implement proper access controls on sensitive directories
- Use strong hashing algorithms (bcrypt, Argon2, scrypt)
- Enforce strong password policies
- Add salt to password hashes
- Implement rate limiting on login attempts
- Use multi-factor authentication for admin accounts
- Never store credentials in accessible files
# Sensitive File Exposure & Weak Credentials

## Vulnerability:
The website exposes sensitive files through robots.txt and uses
weak password hashing with easily crackable credentials.

## Weaknesses Found:
1. robots.txt reveals hidden directories
2. Plaintext username in exposed file
3. MD5 hashed password (weak hashing algorithm)
4. Weak password that exists in common password databases
5. No rate limiting on admin login

## Exploitation Steps:
1. Discovered robots.txt file containing disallowed paths
2. Found /whatever directory listed in robots.txt
3. Accessed the file containing credentials:
   - Username: root
   - Password hash (MD5): 437394baff5aa33daa618be47b75cb49
4. Cracked hash using CrackStation: qwerty123@
5. Logged into /admin with credentials root:qwerty123@
6. Retrieved flag from admin panel

## OWASP Classification:
- A01:2021 - Broken Access Control
- A02:2021 - Cryptographic Failures
- A05:2021 - Security Misconfiguration

## How to Fix:
- Never expose sensitive files in robots.txt
- Use robots.txt only for SEO, not security
- Implement proper access controls on sensitive directories
- Use strong hashing algorithms (bcrypt, Argon2, scrypt)
- Enforce strong password policies
- Add salt to password hashes
- Implement rate limiting on login attempts
- Use multi-factor authentication for admin accounts
- Never store credentials in accessible files