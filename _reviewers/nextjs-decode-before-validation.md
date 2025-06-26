---
title: "Decode before validation"
description: "Always decode URL paths before performing security validations to prevent bypass attacks using URL encoding. Security mechanisms that rely on string pattern matching can be circumvented when attackers use URL-encoded characters."
repository: "vercel/next.js"
label: "Security"
language: "TypeScript"
comments_count: 1
repository_stars: 133000
---

Always decode URL paths before performing security validations to prevent bypass attacks using URL encoding. Security mechanisms that rely on string pattern matching (like `includes()`, `startsWith()`, or regular expressions) can be circumvented when attackers use URL-encoded characters.

For example, instead of:
```javascript
function isSecurePath(url) {
  // VULNERABLE: Can be bypassed with encoding
  return !url.includes('/admin') && !url.includes('/internal');
}
```

Use decoded URLs for validation:
```javascript
function isSecurePath(url) {
  // SECURE: Handles encoded paths
  const decodedUrl = decodeURIComponent(url);
  return !decodedUrl.includes('/admin') && !decodedUrl.includes('/internal');
}
```

This pattern prevents attacks where `/%61dmin` (encoded 'a') would bypass a check for '/admin'. Always normalize URL inputs before security-critical validations to maintain consistent security controls across your application.