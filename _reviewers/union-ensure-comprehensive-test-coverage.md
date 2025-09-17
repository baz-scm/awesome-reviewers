---
title: Ensure comprehensive test coverage
description: All new functionality must include corresponding tests that verify both
  success and failure scenarios. When adding new functions or modifying existing behavior,
  write tests that cover the main functionality as well as edge cases and error conditions.
repository: unionlabs/union
label: Testing
language: Rust
comments_count: 2
repository_stars: 74800
---

All new functionality must include corresponding tests that verify both success and failure scenarios. When adding new functions or modifying existing behavior, write tests that cover the main functionality as well as edge cases and error conditions.

Key requirements:
- New functions should have dedicated tests (like the `execute_burn` function that "needs to be tested to ensure it works correctly")
- Test edge cases and validation logic (such as "sync committee bits vector length is checked correctly")
- Include both positive and negative test cases to ensure proper error handling
- Avoid deploying untested code to production environments

Example of comprehensive test coverage:
```rust
#[test]
fn execute_burn_works() {
    // Test successful burn operation
    let result = execute_burn(deps, env, info, amount);
    assert!(result.is_ok());
}

#[test]
fn execute_burn_fails_with_invalid_amount() {
    // Test edge case with invalid input
    let result = execute_burn(deps, env, info, Uint128::zero());
    assert!(result.is_err());
}

#[test]
fn validate_sync_committee_bits_length() {
    // Test vector length validation
    let mut update = valid_update.clone();
    update.sync_aggregate.sync_committee_bits.clear();
    assert!(validate_update(&update).is_err());
}
```

This practice prevents issues from reaching production and ensures code reliability through thorough validation of all code paths.