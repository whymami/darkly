# Open Redirect via Insecure Redirect Parameter

## Vulnerability
The application uses a redirect function at:
`index.php?page=redirect&site=<value>`  
The value of the **site** parameter is directly used to determine the redirect target without validation.  
This allows attackers to manipulate the parameter and redirect users to arbitrary locations, exposing them to phishing or data exfiltration.

## Weaknesses Found
1. Redirect destination depends on unvalidated user input  
2. Lack of whitelist/validation for `site` parameter  
3. Trusting client-controlled parameters for navigation  
4. Potential for phishing or flag exposure  

## Exploitation Steps
1. Observed legitimate links on the page:
   ```html
   <a href="index.php?page=redirect&site=twitter" class="icon fa-twitter"></a>
   <a href="index.php?page=redirect&site=google" class="icon fa-google"></a>
2. Modified the site parameter manually.

3. Accessed restricted location through crafted URL:
```
 http://104.238.21.89/index.php?page=redirect&site=flag
```

4. Server processed request and returned flag.
```
Flag:

b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f
```
How to Fix

Implement strict validation and allow only whitelisted redirect destinations

Do not rely on client-controlled parameters for navigation logic

Use server-side mappings (e.g., site=1 → twitter.com) instead of passing raw domains

Encode and sanitize all URL parameters

Educate users with proper warning pages before redirecting outside the domain
