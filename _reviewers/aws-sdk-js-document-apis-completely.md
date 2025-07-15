---
title: Document APIs completely
description: 'Always provide complete, clear, and contextually rich documentation
  for all public APIs. Documentation should:


  1. Use proper grammar and clear wording'
repository: aws/aws-sdk-js
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 7628
---

Always provide complete, clear, and contextually rich documentation for all public APIs. Documentation should:

1. Use proper grammar and clear wording
2. Specify environment requirements and version constraints where applicable
3. Be present for all publicly exposed functions, methods, and properties

**Example:**

```typescript
/**
 * Custom DNS lookup function.
 * Defaults to dns.lookup.
 * Used in Node.js (>= v12.x) environment only.
 */
lookupFunction?: LookupFunction;

/**
 * Whether to enable endpoint discovery for operations that allow 
 * optionally using an endpoint returned by the service.
 */
endpointDiscovery?: boolean;
```

Thorough documentation helps other developers understand how to use your code correctly and identify potential limitations or requirements.
