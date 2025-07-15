---
title: "Proper Axios Configuration and Usage"
description: "When implementing code that uses the Axios library in TypeScript, it is important to follow best practices for configuring and accessing Axios instances and settings. Ensure that Axios instances are properly configured with appropriate defaults, configuration properties are accessed correctly, and request-specific configuration overrides instance-level defaults in a predictable manner."
repository: "axios/axios"
label: "Axios"
language: "TypeScript"
comments_count: 3
repository_stars: 107000
---

When implementing code that uses the Axios library in TypeScript, it is important to follow best practices for configuring and accessing Axios instances and settings. Ensure that:

1. Axios instances are properly configured with appropriate defaults, such as timeout values and custom properties.
2. Configuration properties are accessed correctly, using the proper namespacing and access paths.
3. Request-specific configuration overrides instance-level defaults in a predictable manner.

For example, when creating an Axios instance:

```typescript
// GOOD: Clearly document Axios instance configuration
// Configuration precedence order:
// 1. Library defaults
// 2. Instance defaults
// 3. Request-specific config (overrides instance defaults for url, method, params, data)

const instance = axios.create({
  timeout: 5000,
  customConfig: { retryOnError: true } // Custom properties in their own namespace
});

// Access custom config properly
if (config && instance.customConfig.retryOnError) {
  // Handle retry logic
}
```

This ensures that developers working on the codebase understand how Axios configuration is resolved, preventing unexpected behavior from improperly merged settings and maintaining clear separation between standard and custom configuration properties.