---
title: Accept standard objects
description: Design APIs to accept standard object types (like URL and Request) directly,
  not just custom configuration objects. This improves ergonomics by reducing manual
  conversion steps for API consumers and leverages native language features.
repository: axios/axios
label: API
language: Javascript
comments_count: 2
repository_stars: 107146
---

Design APIs to accept standard object types (like URL and Request) directly, not just custom configuration objects. This improves ergonomics by reducing manual conversion steps for API consumers and leverages native language features.

Example:
```javascript
// Good: Flexible API that accepts both configuration objects and standard objects
instance.create = function create(instanceConfigOrUrlOrRequest, instanceConfig) {
  // Handle URL objects directly
  if (instanceConfigOrUrlOrRequest instanceof URL) {
    instanceConfig = configFromURL(instanceConfigOrUrlOrRequest, instanceConfig);
  } 
  // Handle Request objects directly
  else if (isRequest(instanceConfigOrUrlOrRequest)) {
    instanceConfig = configFromRequest(instanceConfigOrUrlOrRequest, instanceConfig);
  }
  
  // Continue with normal flow using the derived or provided config
  return createInstance(mergeConfig(defaultConfig, instanceConfig || instanceConfigOrUrlOrRequest));
}

// Usage:
// Standard way with config object
axios.create({ baseURL: 'https://api.example.com' });
// Enhanced way with URL object
axios.create(new URL('https://api.example.com'));
```

By accepting standard objects directly, your API becomes more intuitive and requires fewer conversions, improving the developer experience while maintaining compatibility with existing code.

## Discussions

