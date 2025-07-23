---
title: Write comprehensive test assertions
description: Instead of making multiple small assertions that check individual fields
  or conditions, write single comprehensive assertions that verify the complete expected
  state. This approach makes tests more maintainable, provides better documentation
  of expected behavior, and makes test failures more informative.
repository: openai/codex
label: Testing
language: Rust
comments_count: 5
repository_stars: 31275
---

Instead of making multiple small assertions that check individual fields or conditions, write single comprehensive assertions that verify the complete expected state. This approach makes tests more maintainable, provides better documentation of expected behavior, and makes test failures more informative.

Example - Instead of:
```rust
assert_eq!(tools[0]["type"], "function");
assert_eq!(tools[0]["name"], "shell");
assert!(tools.iter().any(|t| t.get("name") == Some(&name.clone().into())));
```

Prefer:
```rust
assert_eq!(tools, vec![
    json!({
        "type": "function",
        "name": "shell"
    }),
    json!({
        "type": "function", 
        "name": name
    })
]);
```

This practice:
- Makes the expected state immediately clear
- Reduces test maintenance overhead
- Effectively documents the complete expected behavior
- Makes test failures more informative by showing all differences at once
- Serves as living documentation of the expected wire format/data structures

When dealing with complex objects that don't implement PartialEq, consider implementing it to enable comprehensive assertions rather than checking fields individually.