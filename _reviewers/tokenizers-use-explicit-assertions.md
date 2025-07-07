---
title: Use explicit assertions
description: Tests should assert specific expected values rather than just verifying
  general functionality. This practice makes tests more robust against subtle regressions
  and helps catch "under the radar" bugs where behavior is modified unintentionally.
repository: huggingface/tokenizers
label: Testing
language: Rust
comments_count: 2
repository_stars: 9868
---

Tests should assert specific expected values rather than just verifying general functionality. This practice makes tests more robust against subtle regressions and helps catch "under the radar" bugs where behavior is modified unintentionally.

Instead of print statements or simply checking that code runs without errors, include explicit assertions that verify exact expected outputs:

```rust
// LESS ROBUST: Only verifies the code runs without errors
#[test]
fn test_tokenizer() {
    let output = tokenizer.encode("Hello", true).unwrap();
    println!("{:?}", output.get_tokens()); // Just prints, doesn't verify
}

// MORE ROBUST: Explicitly checks expected values
#[test]
fn test_tokenizer() {
    let output = tokenizer.encode("Hello", true).unwrap();
    assert_eq!(
        output.get_tokens(), 
        ["[CLS]", "Hello", "[SEP]"]
    );
    assert_eq!(
        output.get_ids(),
        [1, 27253, 2]
    );
}
```

This approach creates tests that serve as both verification and documentation of expected behavior. While it may require more maintenance when intentionally changing behavior, it significantly improves the ability to catch unintended changes and regressions.