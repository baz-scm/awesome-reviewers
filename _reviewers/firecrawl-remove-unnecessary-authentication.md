---
title: remove unnecessary authentication
description: Avoid initializing authentication mechanisms, credentials, or identity
  objects when they are not actually used in the code. This follows the security principle
  of least privilege and reduces potential attack surface by minimizing credential
  exposure.
repository: firecrawl/firecrawl
label: Security
language: TypeScript
comments_count: 1
repository_stars: 54535
---

Avoid initializing authentication mechanisms, credentials, or identity objects when they are not actually used in the code. This follows the security principle of least privilege and reduces potential attack surface by minimizing credential exposure.

In test files particularly, only set up authentication when the test actually makes API calls or requires authenticated operations. Unnecessary authentication setup can lead to credential leakage and violates security best practices.

Example of what to avoid:
```typescript
// Bad: Creating identity when no API calls are made
let identity: Identity;
beforeAll(async () => {
  identity = await idmux({
    name: "robots-txt", 
    concurrency: 100,
    credits: 1000000,
  });
});

// Good: Remove unused authentication setup
// (no identity initialization needed if no API calls)
```

Always review whether authentication setup is actually necessary for the functionality being implemented or tested.