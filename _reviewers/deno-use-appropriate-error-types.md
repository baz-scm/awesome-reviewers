---
title: Use appropriate error types
description: Functions should use specific, appropriate error handling mechanisms
  rather than generic or brittle approaches. This includes returning proper error
  codes when operations fail, using specific error types instead of generic `notImplemented`
  errors, and avoiding fragile error detection methods like string matching.
repository: denoland/deno
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 103714
---

Functions should use specific, appropriate error handling mechanisms rather than generic or brittle approaches. This includes returning proper error codes when operations fail, using specific error types instead of generic `notImplemented` errors, and avoiding fragile error detection methods like string matching.

Key practices:
- Return meaningful error codes when operations can fail, not just success values
- Use specific error types that accurately represent the failure condition
- Avoid brittle error detection like `e.message === "cancelled"` - prefer proper error type checking
- Add appropriate safeguards (timeouts, limits) to prevent hanging in failure scenarios

Example of improvement:
```typescript
// Instead of always returning success:
setBroadcast(_bool: 0 | 1): number {
  this.#listener?.setBroadcast(_bool === 1);
  return 0; // Always success - problematic
}

// Return appropriate error codes:
setBroadcast(_bool: 0 | 1): number {
  try {
    this.#listener?.setBroadcast(_bool === 1);
    return 0;
  } catch {
    return -1; // Proper error indication
  }
}

// Instead of generic errors:
export function setFipsCrypto(_fips: boolean) {
  notImplemented("crypto.setFipsCrypto"); // Generic
}

// Use specific error types:
export function setFipsCrypto(_fips: boolean) {
  throw new Error("FIPS mode is not available"); // Specific
}
```