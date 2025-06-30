---
title: Validate request inputs
description: Always validate and sanitize user-provided inputs that affect HTTP requests
  or responses to prevent security vulnerabilities like Cross-Site Scripting (XSS)
  and Server-Side Request Forgery (SSRF).
repository: axios/axios
label: Security
language: Javascript
comments_count: 3
repository_stars: 107146
---

Always validate and sanitize user-provided inputs that affect HTTP requests or responses to prevent security vulnerabilities like Cross-Site Scripting (XSS) and Server-Side Request Forgery (SSRF).

For XSS prevention, ensure user inputs aren't reflected in responses without proper encoding. For SSRF prevention, validate URL parameters, paths, and query strings to ensure they cannot be manipulated to target unintended hosts.

Example of vulnerable code:
```javascript
// VULNERABLE: User input directly incorporated into URL
const userId = req.params.userId; // Could be "/localhost:malicious-port"
axios.get(`/${userId}`);

// VULNERABLE: Parameter serialization without validation
axios.get('/', {
  params: {
    userInput: unsanitizedUserInput
  }
});
```

Secure approach:
```javascript
// SECURE: Validate user inputs before using in requests
const userId = req.params.userId;
if (!/^[a-zA-Z0-9]+$/.test(userId)) {
  throw new Error('Invalid userId format');
}
axios.get(`/users/${userId}`);

// For URL parameters, use a validation function
const paramsSerializer = (params) => {
  // Validate and sanitize each parameter
  return Object.entries(params)
    .map(([key, value]) => {
      // Validate value is safe
      if (typeof value !== 'string' || !isSafeValue(value)) {
        throw new Error(`Invalid parameter value for ${key}`);
      }
      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
    })
    .join('&');
};

axios.get('/', {
  params: userParams,
  paramsSerializer
});
```

For complete protection, implement input validation at all entry points and consider using security libraries specific to your framework.

## Discussions

