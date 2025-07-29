---
title: Document cryptographic requirements
description: Security-critical functions, especially those involving cryptographic
  operations, must include clear and accurate documentation about their security requirements
  and assumptions. This is essential for preventing misuse that could lead to vulnerabilities.
repository: vlang/v
label: Security
language: Other
comments_count: 1
repository_stars: 36582
---

Security-critical functions, especially those involving cryptographic operations, must include clear and accurate documentation about their security requirements and assumptions. This is essential for preventing misuse that could lead to vulnerabilities.

When documenting cryptographic functions:
- Explicitly state security requirements for inputs (e.g., "seed bytes must come from a cryptographically secure random generator")
- Use precise, grammatically correct language to avoid ambiguity
- Document any security assumptions or constraints
- Provide guidance on proper usage to prevent security mistakes

Example from ECDSA key generation:
```v
// new_key_from_seed creates a new private key from the seed bytes.
//
// Notes on the seed:
// You should make sure the seed bytes come from a cryptographically secure random generator,
```

Poor documentation of cryptographic requirements can lead developers to make incorrect assumptions about security properties, potentially introducing vulnerabilities through improper usage of otherwise secure cryptographic primitives.