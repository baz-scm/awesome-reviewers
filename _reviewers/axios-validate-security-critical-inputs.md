---
title: "Validate security-critical inputs"
description: "Always validate and sanitize user-supplied inputs before using them in security-sensitive operations. This helps prevent multiple types of vulnerabilities including Server-Side Request Forgery (SSRF), prototype pollution, and command injection."
repository: "axios/axios"
label: "Security"
language: "JavaScript"
comments_count: 4
repository_stars: 107000
---

Always validate and sanitize user-supplied inputs before using them in security-sensitive operations. This helps prevent multiple types of vulnerabilities including Server-Side Request Forgery (SSRF), prototype pollution, and command injection.

For URL validation to prevent SSRF attacks:
```javascript
// When handling user input that affects URLs
try {
  const ssrfAxios = axios.create({
    baseURL: 'http://localhost:' + String(GOOD_PORT),
  });
  
  // Validate user input before using in URL paths
  const userId = validateInput(userSuppliedId);
  
  // If validation fails, throw specific error
  if (!isValidUserId(userId)) {
    throw new Error('Invalid URL:' + userId);
  }
  
  const response = await ssrfAxios.get(`/users/${userId}`);
} catch (error) {
  // Handle error appropriately
}
```

For object property validation to prevent prototype pollution:
```javascript
function isPrototypePollutionAttempt(key) {
  // Check for common prototype pollution patterns
  return ['__proto__', 'constructor', 'prototype'].some(
    term => key === term || key.includes('.' + term)
  );
}

// Use when processing user inputs into objects
function safeAddProperty(obj, key, value) {
  if (isPrototypePollutionAttempt(key)) {
    throw new Error('Potential prototype pollution detected');
  }
  obj[key] = value;
}
```

When using user input in command execution contexts, always use parameterized approaches instead of string concatenation to prevent command injection.