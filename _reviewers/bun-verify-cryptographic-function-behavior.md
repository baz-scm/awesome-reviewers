---
title: Verify cryptographic function behavior
description: When implementing cryptographic algorithms, always verify the exact behavior
  and return values of security-critical functions. Misinterpreting how functions
  signal success or equality can lead to severe security vulnerabilities.
repository: oven-sh/bun
label: Security
language: C++
comments_count: 1
repository_stars: 79093
---

When implementing cryptographic algorithms, always verify the exact behavior and return values of security-critical functions. Misinterpreting how functions signal success or equality can lead to severe security vulnerabilities.

In particular:
- Confirm whether comparison functions return true/false or 0/non-0 for equality
- Implement security checks with precise understanding of function semantics
- Follow relevant cryptographic standards (RFCs) meticulously
- Use constant-time operations for cryptographic comparisons to prevent timing attacks

Example of a potential error in a security check:
```cpp
// INCORRECT: Misinterpreting constantTimeMemcmp which returns 0 for equality
if (derivedKey->size() != expectedOutputSize || !constantTimeMemcmp(derivedKey->span(), zeros)) {
    // Handle insecure all-zeros key case
}

// CORRECT: Properly checking for equality with constantTimeMemcmp
if (derivedKey->size() != expectedOutputSize || constantTimeMemcmp(derivedKey->span(), zeros) == 0) {
    // Handle insecure all-zeros key case
}
```

Security-critical checks must be implemented correctly the first time - cryptographic vulnerabilities can be subtle and devastating.