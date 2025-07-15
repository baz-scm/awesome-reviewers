---
title: Network API compatibility
description: When implementing networking APIs that mirror Node.js functionality,
  ensure both behavior and error patterns match Node.js exactly. This is critical
  for maintaining compatibility with the Node.js ecosystem and ensuring that code
  works consistently across both environments.
repository: oven-sh/bun
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 79093
---

When implementing networking APIs that mirror Node.js functionality, ensure both behavior and error patterns match Node.js exactly. This is critical for maintaining compatibility with the Node.js ecosystem and ensuring that code works consistently across both environments.

Key areas to check for compatibility include:
- Accurate syscall documentation (e.g., using `send(2)` rather than `sendto(2)` for TCP sockets)
- Method signatures and property descriptors that match Node.js
- Identical error types and error conditions
- Equivalent validation logic for parameters

For example, when validating TLS ciphers, ensure the logic matches Node.js behavior by only throwing when no ciphers match (not when any individual cipher is unsupported):

```javascript
// INCORRECT - throws if any cipher isn't supported
const requested = options.ciphers.split(":");
for (const r of requested) {
  if (!DEFAULT_CIPHERS_SET.has(r)) {
    throw $ERR_SSL_NO_CIPHER_MATCH();
  }
}

// CORRECT - matches Node.js behavior by only throwing if no ciphers match
const requested = options.ciphers.split(":");
let hasMatch = false;
for (const r of requested) {
  if (DEFAULT_CIPHERS_SET.has(r)) {
    hasMatch = true;
    break;
  }
}
if (!hasMatch) {
  throw $ERR_SSL_NO_CIPHER_MATCH();
}
```

Always reference the Node.js implementation when implementing networking APIs to ensure consistent behavior across runtime environments.