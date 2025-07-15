---
title: Use secure hash algorithms
description: Always use strong, modern cryptographic hash algorithms for security-sensitive
  operations. Avoid deprecated or weak algorithms that might be vulnerable to attacks.
  When selecting hash algorithms, consider both security requirements and performance
  characteristics.
repository: nestjs/nest
label: Security
language: TypeScript
comments_count: 1
repository_stars: 71767
---

Always use strong, modern cryptographic hash algorithms for security-sensitive operations. Avoid deprecated or weak algorithms that might be vulnerable to attacks. When selecting hash algorithms, consider both security requirements and performance characteristics.

For general hashing needs, prefer SHA-256 over older algorithms like SHA-1 or MD5, which have known vulnerabilities. As demonstrated in the benchmark, SHA-256 often offers better performance alongside stronger security:

```typescript
// Avoid weak algorithms
// BAD:
return xxh32(value).toString();

// GOOD:
return createHash('sha256').update(value).digest('hex');
```

This change not only improves security by using a cryptographically stronger algorithm but can also improve performance. Security scanning tools often flag the use of deprecated cryptographic functions, so following this practice helps prevent security vulnerabilities while maintaining or enhancing application performance.