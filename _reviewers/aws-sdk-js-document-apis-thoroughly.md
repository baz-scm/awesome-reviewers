---
title: Document APIs thoroughly
description: All public API elements must be thoroughly documented with JSDoc annotations
  that clearly explain their purpose, parameters, return values, and default behaviors.
  Documentation should be precise, matching the actual code behavior rather than making
  assumptions or using misleading descriptions.
repository: aws/aws-sdk-js
label: Documentation
language: JavaScript
comments_count: 6
repository_stars: 7628
---

All public API elements must be thoroughly documented with JSDoc annotations that clearly explain their purpose, parameters, return values, and default behaviors. Documentation should be precise, matching the actual code behavior rather than making assumptions or using misleading descriptions.

When adding new parameters or methods:
1. Include comprehensive JSDoc annotations
2. Explain the purpose clearly (not just the type)
3. Document default values
4. Add usage examples for complex features

For example, when adding a new configuration option:

```javascript
/**
 * @!attribute signatureCache
 *   @return [Boolean] whether the signature to sign requests with (overriding
 *     the API configuration) is cached. Only applies to the signature version 'v4'.
 *     Defaults to `true`.
 */

/**
 * @option options signatureCache [Boolean] whether the signature to sign
 *   requests with (overriding the API configuration) is cached. Only applies
 *   to the signature version 'v4'. Defaults to `true`.
 */
```

For methods that return promises, clearly document what the promise resolves to:

```javascript
/**
 * @!method getSignedUrlPromise()
 *   Returns a 'thenable' promise that will be resolved with a pre-signed URL.
 */
```

Ensure that if you're making an API public, all necessary documentation is added and the component is properly exported so it appears in generated documentation.
