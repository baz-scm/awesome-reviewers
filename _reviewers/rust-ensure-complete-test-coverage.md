---
title: Ensure complete test coverage
description: 'Write comprehensive tests that cover all relevant cases and variations
  while maintaining proper organization and structure. Key practices:


  1. Place tests in appropriate locations (e.g., core tests in `library/coretests`)'
repository: rust-lang/rust
label: Testing
language: Rust
comments_count: 7
repository_stars: 105254
---

Write comprehensive tests that cover all relevant cases and variations while maintaining proper organization and structure. Key practices:

1. Place tests in appropriate locations (e.g., core tests in `library/coretests`)
2. Include FileCheck annotations for validation
3. Test both positive and negative cases separately
4. Cover analogous behaviors and backwards compatibility
5. Structure tests within proper test functions

Example:
```rust
// In library/coretests/your_module.rs
#[test]
fn test_feature_behavior() {
    // Test primary functionality
    let result = do_something();
    assert_eq!(result.primary(), expected);
    
    // Test analogous case
    let alt_result = do_something_similar();
    assert_eq!(alt_result.similar(), expected);
    
    // Test backwards compatibility
    assert_eq!(result.legacy_method(), old_expected);
    assert_eq!(result.new_method(), new_expected);
}

// Separate file for failure cases
// In tests/ui/your_module_failures.rs
//@ build-fail
//@ ignore-pass
fn test_invalid_case() {
    // Test expected failure
    let result = invalid_operation();
    //~^ ERROR expected error message
}
```