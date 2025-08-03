---
title: Sanitize user inputs
description: "Always validate and sanitize user-provided inputs before using them\
  \ in security-sensitive operations to prevent XSS attacks and unsafe redirections.\
  \ \n"
repository: RooCodeInc/Roo-Code
label: Security
language: JavaScript
comments_count: 2
repository_stars: 17288
---

Always validate and sanitize user-provided inputs before using them in security-sensitive operations to prevent XSS attacks and unsafe redirections. 

When handling URLs from user input:
- Use proper URL parsing and validation
- Restrict to safe protocols (typically only http: and https:)
- Consider using URL allowlists for sensitive operations

When inserting content into the DOM:
- Always escape HTML special characters
- Use textContent instead of innerHTML when possible
- Consider using sanitization libraries like DOMPurify

Example (improved URL validation):
```javascript
function loadUrl(url) {
  try {
    // Parse and validate URL
    const urlObj = new URL(url, window.location.origin);
    
    // Only allow http and https protocols
    if (urlObj.protocol !== 'http:' && urlObj.protocol !== 'https:') {
      console.error('Invalid URL protocol');
      return;
    }
    
    // Use the validated URL
    iframe.src = urlObj.toString();
  } catch (e) {
    console.error('Invalid URL format', e);
  }
}
```

This practice helps prevent client-side open redirect vulnerabilities and cross-site scripting (XSS) attacks that could compromise user security.