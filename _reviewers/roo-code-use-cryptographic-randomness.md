---
title: Use cryptographic randomness
description: Always use cryptographically secure random number generation for security-sensitive
  operations such as generating session IDs, authentication tokens, or unique identifiers.
  Standard random number generators like `Math.random()` are designed for statistical
  randomness, not security, making them vulnerable to prediction and exploitation
  by attackers.
repository: RooCodeInc/Roo-Code
label: Security
language: TypeScript
comments_count: 3
repository_stars: 17288
---

Always use cryptographically secure random number generation for security-sensitive operations such as generating session IDs, authentication tokens, or unique identifiers. Standard random number generators like `Math.random()` are designed for statistical randomness, not security, making them vulnerable to prediction and exploitation by attackers.

```typescript
// Insecure - using Math.random() for session IDs:
const sessionId = `roo-${Date.now()}-${Math.random().toString(36).substring(7)}`;

// Secure - using cryptographic randomness:
import crypto from 'crypto';
// In Node.js:
const sessionId = `roo-${Date.now()}-${crypto.randomBytes(16).toString('hex')}`;
// OR
const sessionId = `roo-${Date.now()}-${crypto.randomUUID()}`;
```

For browser environments, use the Web Crypto API:
```javascript
// Browser environment:
const array = new Uint8Array(16);
window.crypto.getRandomValues(array);
const sessionId = `roo-${Date.now()}-${Array.from(array).map(b => b.toString(16).padStart(2, '0')).join('')}`;
```

Predictable randomness can lead to session hijacking, token guessing, and other security vulnerabilities that may compromise user data or system integrity.