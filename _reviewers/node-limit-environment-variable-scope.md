---
title: Limit environment variable scope
description: 'When working with environment variables for configuration:


  1. **Reuse existing environment variables** rather than creating new ones. Leverage
  established variables like `NODE_TEST_CONTEXT` where possible to avoid fragmentation.'
repository: nodejs/node
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 112178
---

When working with environment variables for configuration:

1. **Reuse existing environment variables** rather than creating new ones. Leverage established variables like `NODE_TEST_CONTEXT` where possible to avoid fragmentation.

2. **Extract only necessary environment variables** instead of passing the entire environment. This improves security and makes dependencies explicit.

```javascript
// Avoid:
proxyEnv: process.env.NODE_USE_ENV_PROXY ? process.env : undefined,

// Prefer:
proxyEnv: process.env.NODE_USE_ENV_PROXY ? {
  HTTP_PROXY: process.env.HTTP_PROXY,
  HTTPS_PROXY: process.env.HTTPS_PROXY,
  NO_PROXY: process.env.NO_PROXY
} : undefined,
```

3. **Check environment variables consistently** and be mindful of truthiness. Remember that environment variables are strings or undefined, and plan accordingly.

4. **Document new environment variables** if you absolutely must create them, and ensure they follow established naming conventions for your project.