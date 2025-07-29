---
title: Document algorithm behavior
description: When implementing or documenting algorithms, clearly specify their behavior,
  expected outputs, and usage patterns. This includes documenting mathematical operation
  semantics, output characteristics, and providing complete examples that demonstrate
  the algorithm's behavior.
repository: vlang/v
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 36582
---

When implementing or documenting algorithms, clearly specify their behavior, expected outputs, and usage patterns. This includes documenting mathematical operation semantics, output characteristics, and providing complete examples that demonstrate the algorithm's behavior.

Key aspects to document:
- **Mathematical behavior**: Specify how operations behave with different inputs (e.g., "the sign of the remainder depends upon the signs of divisor and dividend")
- **Output characteristics**: Document the size, format, and properties of algorithm outputs (e.g., "shared secret is 32 bytes length")
- **Sequential patterns**: For algorithms that generate sequences, specify the starting values and progression (e.g., "values start at 0 and increase by 1")
- **Usage examples**: Provide complete examples showing expected results

Example from cryptographic algorithm documentation:
```v
// Alice derives shared secret with her own private key with Bob's public key
alice_shared_sec := curve25519.derive_shared_secret(mut alice_pvkey, bob_pbkey)!

// Bob derives shared secret with his own private key with Alice's public key  
bob_shared_sec := curve25519.derive_shared_secret(mut bob_pvkey, alice_pbkey)!

// the two shared secrets (derived by Alice, and derived by Bob), should be the same
// Output: 32-byte shared secret
println('Alice secret: ${alice_shared_sec}')
println('Bob secret: ${bob_shared_sec}')
```

This ensures developers understand not just how to use the algorithm, but what to expect from it and how it behaves in different scenarios.