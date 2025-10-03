# Hidden Directory Enumeration & Information Disclosure

## Vulnerability:
The website exposes a hidden directory structure through robots.txt
containing thousands of subdirectories with README files. One of these
files contains sensitive information (the flag). This represents poor
security through obscurity and information disclosure.

## Weaknesses Found:
1. Security through obscurity (hidden directories disclosed in robots.txt)
2. No proper access control on hidden directories
3. Directory listing enabled
4. Sensitive information stored in accessible locations
5. Predictable directory structure
6. robots.txt used incorrectly for "hiding" sensitive content
7. Information disclosure through README files

## Discovery Method:
1. Checked robots.txt file
2. Found /.hidden/ directory listed as disallowed
3. Accessed the directory and found thousands of nested subdirectories
4. Each directory contained a README file
5. Most README files contained decoy messages in French
6. Had to crawl all directories to find the real flag

## Exploitation Steps:
1. Accessed http://[IP]/robots.txt
2. Found:User-agent: *
Disallow: /whatever
Disallow: /.hidden
3. Navigated to /.hidden/ directory
4. Discovered nested directory structure with README files
5. Wrote Python async crawler to scan all directories
6. Collected all unique README files (MD5 deduplication)
7. Found flag in: /.hidden/whtccjokayshttvxycsvykxcfm/igeemtxnvexvxezqwntmzjltkt/lmpanswobhwcozdqixbowvbrhw/README

## Decoy Messages Found:
- "Tu veux de l'aide ? Moi aussi !" (You want help? Me too!)
- "Demande à ton voisin de droite" (Ask your right neighbor)
- "Demande à ton voisin du dessus" (Ask your neighbor above)
- "Demande à ton voisin du dessous" (Ask your neighbor below)
- "Non ce n'est toujours pas bon ..." (No, it's still not right...)

## OWASP Classification:
- A01:2021 - Broken Access Control
- A05:2021 - Security Misconfiguration
- A07:2021 - Identification and Authentication Failures

## How to Fix:
1. Access Control:
   - Implement proper authentication and authorization
   - Use server configuration to deny access to sensitive directories
   - Never rely on obscurity for security
   - robots.txt does NOT provide security - it only tells search engines what not to index

2. Directory Security:
   - Disable directory listing
   - Use proper file permissions
   - Store sensitive files outside web root
   - Implement proper access controls at the application level

3. Best Practices:
   - Don't store sensitive information in web-accessible locations
   - robots.txt is for SEO, not security
   - Implement rate limiting to prevent mass crawling
   - Monitor access logs for enumeration attempts
   - Use Web Application Firewall (WAF)
   - Never list sensitive directories in robots.txt