---
title: prefer standard crypto functions
description: Use Node.js built-in crypto module functions instead of third-party cryptographic
  libraries when possible. The built-in crypto module is well-maintained, follows
  established standards, and provides better security guarantees than external alternatives.
repository: cloudflare/workers-sdk
label: Security
language: TypeScript
comments_count: 1
repository_stars: 3379
---

Use Node.js built-in crypto module functions instead of third-party cryptographic libraries when possible. The built-in crypto module is well-maintained, follows established standards, and provides better security guarantees than external alternatives.

Standard crypto functions are more likely to receive security updates, have been thoroughly vetted, and reduce dependency risks. They also provide consistent behavior across different environments.

Example:
```javascript
// Prefer this
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update(data).digest('hex');

// Instead of
const hash = blake3hash(data).toString('hex');
```

This applies to hash functions, encryption, and other cryptographic operations where Node.js provides built-in alternatives.