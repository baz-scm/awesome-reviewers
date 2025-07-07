---
title: Assert exact expectations
description: Always assert exact expected values in tests rather than using loose
  assertions. When testing the presence of elements or count of items, use equality
  assertions (`assert_eq!`) instead of non-empty checks (`assert!(!items.is_empty())`)
  or inequality assertions (`assert!(items.len() >= 2)`).
repository: astral-sh/ruff
label: Testing
language: Rust
comments_count: 3
repository_stars: 40619
---

Always assert exact expected values in tests rather than using loose assertions. When testing the presence of elements or count of items, use equality assertions (`assert_eq!`) instead of non-empty checks (`assert!(!items.is_empty())`) or inequality assertions (`assert!(items.len() >= 2)`).

Exact assertions:
- Make test failures more informative by showing the expected and actual values
- Prevent silent test degradation when code changes affect output quantity
- Catch unexpected behavior that looser assertions would miss

For example, instead of:

```rust
// Testing that some tokens exist (too loose)
let class_tokens = tokens.iter()
    .filter(|t| matches!(t.token_type, SemanticTokenType::Class))
    .collect();
assert!(!class_tokens.is_empty());

// Using inequality (can hide issues)
let variable_tokens = tokens.iter()
    .filter(|t| matches!(t.token_type, SemanticTokenType::Variable))
    .collect();
assert!(variable_tokens.len() >= 2);
```

Use this approach instead:

```rust
// Test for the exact expected count
let class_tokens = tokens.iter()
    .filter(|t| matches!(t.token_type, SemanticTokenType::Class))
    .collect();
assert_eq!(class_tokens.len(), 1);

// Or use a helper function for multiple assertions
assert_token_count([
    (SemanticTokenType::BuiltinConstant, 3),
    (SemanticTokenType::Variable, 3),
]);
```

When practical, consider extracting assertions into helper functions that verify the exact composition of test results, making tests more readable and consistent.