---
title: validate input constraints
description: Always validate user inputs against expected formats, constraints, and
  business rules before processing them. Implement explicit validation checks that
  fail fast with clear error messages when inputs don't meet requirements. This prevents
  security vulnerabilities from malformed or malicious inputs.
repository: unionlabs/union
label: Security
language: TypeScript
comments_count: 1
repository_stars: 74800
---

Always validate user inputs against expected formats, constraints, and business rules before processing them. Implement explicit validation checks that fail fast with clear error messages when inputs don't meet requirements. This prevents security vulnerabilities from malformed or malicious inputs.

Example from Bech32 address validation:
```typescript
Effect.flatMap(decoded => {
  if (decoded.prefix !== prefix) {
    return Effect.fail(
      new Bech32DecodeError({
        message: `Given prefix "${decoded.prefix}" does not match requirement "${prefix}"`,
      }),
    )
  }
  // Continue processing only after validation passes
})
```

This approach is especially critical for user-facing inputs like addresses, identifiers, and configuration values that could be manipulated to exploit system vulnerabilities.