---
title: validate input uniqueness
description: Always validate that input data is unique and matches expected values
  to prevent replay attacks and data manipulation vulnerabilities. This includes checking
  for duplicate submissions and verifying data integrity through hash comparisons.
repository: unionlabs/union
label: Security
language: Rust
comments_count: 2
repository_stars: 74800
---

Always validate that input data is unique and matches expected values to prevent replay attacks and data manipulation vulnerabilities. This includes checking for duplicate submissions and verifying data integrity through hash comparisons.

Key validation patterns:
1. **Prevent duplicate data attacks**: Ensure that the same data cannot be submitted multiple times to create false evidence or bypass security checks
2. **Verify data consistency**: Confirm that related data fields match expected values (e.g., block hashes match attestation data)
3. **Implement uniqueness checks**: Add explicit validation to reject identical inputs that could be used maliciously

Example implementation:
```rust
// Prevent duplicate attestation attacks
if misbehaviour.attestation_1.number != misbehaviour.attestation_2.number {
    // Additional checks needed here to ensure attestations are truly different
    // and not the same data provided twice
}

// Verify hash consistency  
if block.hash() != vote_attestation.data.source_hash {
    return Err(Error::HashMismatch);
}
```

This validation is critical for preventing attackers from exploiting duplicate or inconsistent data to bypass security mechanisms or create false evidence of misbehaviour.