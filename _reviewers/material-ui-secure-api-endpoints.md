---
title: Secure API endpoints
description: 'Always implement appropriate security measures for API endpoints that
  perform sensitive operations. This includes:


  1. **Verify request authenticity**: Ensure requests come from legitimate sources
  using mechanisms like SDK verification, API keys, or signatures.'
repository: mui/material-ui
label: Security
language: JavaScript
comments_count: 2
repository_stars: 96063
---

Always implement appropriate security measures for API endpoints that perform sensitive operations. This includes:

1. **Verify request authenticity**: Ensure requests come from legitimate sources using mechanisms like SDK verification, API keys, or signatures.

2. **Validate HTTP methods**: Restrict non-idempotent operations (create/update/delete) to appropriate methods like POST, and reject GET/HEAD requests for these operations.

Example:
```javascript
exports.handler = async (event) => {
  // 1. Verify HTTP method
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 404,
      body: 'Not found'
    };
  }
  
  // 2. Verify request authenticity
  // Using SDK verification or custom validation
  const isAuthentic = verifyRequestSignature(event);
  if (!isAuthentic) {
    return {
      statusCode: 401,
      body: 'Unauthorized request'
    };
  }
  
  // Continue with handling the authenticated request
  // ...
}
```

These measures prevent unauthorized access and protect against security exploits where sensitive operations might be triggered unintentionally through link following, bots, or prefetching.