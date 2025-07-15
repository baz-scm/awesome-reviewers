---
title: Enforce HTTPS protocol
description: Always validate that URLs use the HTTPS protocol in both implementation
  code and validation error messages. Even if your application might handle HTTP-to-HTTPS
  redirects, enforce HTTPS from the outset as a security best practice to prevent
  man-in-the-middle attacks and data exposure.
repository: kubeflow/kubeflow
label: Security
language: TypeScript
comments_count: 1
repository_stars: 15064
---

Always validate that URLs use the HTTPS protocol in both implementation code and validation error messages. Even if your application might handle HTTP-to-HTTPS redirects, enforce HTTPS from the outset as a security best practice to prevent man-in-the-middle attacks and data exposure.

Example:
```javascript
// Incorrect - allows HTTP
if (!/^https?:\/\/\S+/.test(url)) {
  console.log('Invalid URL provided, must be like http*://*');
  return false;
}

// Correct - enforces HTTPS only
if (!/^https:\/\/\S+/.test(url)) {
  console.log('Invalid URL provided, must use HTTPS protocol');
  return false;
}
```

This helps ensure all communications are encrypted and prevents security vulnerabilities that can arise from initial insecure connections.
