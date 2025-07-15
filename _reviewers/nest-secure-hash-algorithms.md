---
title: Secure hash algorithms
description: Always use cryptographically secure hash algorithms for sensitive operations
  instead of weak or broken ones. Weak algorithms can compromise security and make
  your application vulnerable. Prefer modern algorithms like SHA-256 over older or
  non-cryptographic hash functions.
repository: nestjs/nest
label: Security
language: TypeScript
comments_count: 1
repository_stars: 71766
---

Always use cryptographically secure hash algorithms for sensitive operations instead of weak or broken ones. Weak algorithms can compromise security and make your application vulnerable. Prefer modern algorithms like SHA-256 over older or non-cryptographic hash functions.

When selecting a hashing algorithm, consider both security requirements and performance implications. As demonstrated in the benchmarks, sometimes the more secure option may also offer better performance:

```typescript
// Avoid using weak hashing algorithms
// AVOID: return xxh32(value).toString();

// PREFER: Use cryptographically secure algorithms
return createHash('sha256').update(value).digest('hex');
```

Note that non-cryptographic hash functions (like xxhash) are designed for speed and collision resistance in data structures, but not for security purposes where resistance to attacks is required.