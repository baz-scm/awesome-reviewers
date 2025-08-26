---
title: Write explicit concrete tests
description: Tests should be written explicitly with concrete examples and clear assertions
  rather than being generated programmatically or hidden in utility code. This improves
  test readability, maintainability, and debugging capabilities.
repository: tree-sitter/tree-sitter
label: Testing
language: Rust
comments_count: 3
repository_stars: 21799
---

Tests should be written explicitly with concrete examples and clear assertions rather than being generated programmatically or hidden in utility code. This improves test readability, maintainability, and debugging capabilities.

Key principles:
- Add meaningful assertions to documentation tests, not just setup code
- Write hand-crafted test cases with specific expected outcomes instead of loop-generated tests
- Place test validation logic in proper unit tests rather than utility functions
- Make test intentions clear through concrete examples

Example of preferred approach:
```rust
// Instead of generated tests in loops
#[test]
fn test_consecutive_zero_or_modifiers() {
    // Prefer explicit test cases
    let query1 = Query::new(language, "(comment)*** @capture").unwrap();
    let query2 = Query::new(language, "(comment)??? @capture").unwrap();
    
    // With specific assertions about expected behavior
    assert_eq!(matches1.len(), 3);
    assert_eq!(matches2.len(), 1);
}

// Add assertions to doc tests
//! let tree = parser.parse(code, None).unwrap();
//! assert!(!tree.root_node().has_error());
```

This approach makes tests easier to understand, debug, and maintain while ensuring that test behavior is predictable and well-documented.