---
title: Node.js API compatibility
description: When implementing Node.js-compatible APIs, ensure exact behavioral matching
  with Node.js, including export structures, method signatures, return types, and
  property availability. This maintains compatibility with existing Node.js code and
  meets developer expectations.
repository: cloudflare/workerd
label: API
language: TypeScript
comments_count: 6
repository_stars: 6989
---

When implementing Node.js-compatible APIs, ensure exact behavioral matching with Node.js, including export structures, method signatures, return types, and property availability. This maintains compatibility with existing Node.js code and meets developer expectations.

Key areas to verify:
- **Default exports**: Match Node.js module export patterns (e.g., `node:module` should export `Module` as default)
- **Method availability**: Implement expected methods even as no-ops to prevent runtime errors (e.g., `server.address().port` for logging code)
- **Property structures**: Ensure objects have the same shape and property names as Node.js equivalents
- **Version-specific behavior**: Use appropriate compatibility flags to match Node.js version behavior (e.g., deprecated APIs exported as `undefined` in newer versions)

Example from the discussions:
```typescript
// Correct: Match Node.js default export expectation
export default Module; // Instead of object with methods

// Correct: Provide expected methods even if not fully implemented
server.address(): AddressInfo | string | null {
  return { port: this.port, family: 'IPv4', address: '0.0.0.0' };
}

// Correct: Use version-appropriate compatibility flags
if (!Cloudflare.compatibilityFlags.remove_nodejs_compat_eol_v22) {
  // Export as undefined in v22 to match Node.js behavior
}
```

This ensures seamless migration of existing Node.js applications and prevents unexpected runtime failures due to missing properties or methods.