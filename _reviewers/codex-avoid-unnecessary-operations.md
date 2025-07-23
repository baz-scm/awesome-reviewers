---
title: Avoid unnecessary operations
description: 'Optimize performance by eliminating operations that don''t contribute
  meaningful value to your code''s functionality. Look for three common performance
  drains:'
repository: openai/codex
label: Performance Optimization
language: Rust
comments_count: 3
repository_stars: 31275
---

Optimize performance by eliminating operations that don't contribute meaningful value to your code's functionality. Look for three common performance drains:

1. **Redundant I/O operations**: Avoid unnecessary file system operations like flushing a file that has already been flushed or has no new content.
   
2. **Excessive UI rendering**: Implement throttling at the appropriate architectural level rather than in individual components. Consider centralizing performance controls in higher-level components where they can be applied globally.

3. **Unnecessary memory allocations**: Use references or smarter allocation patterns instead of blindly cloning data structures.

```rust
// Instead of always cloning:
let prompt = if missing_calls.is_empty() {
    prompt.clone()
    // ...
}

// Use Cow to avoid unnecessary cloning:
let prompt: Cow<'_, Prompt> = if missing_calls.is_empty() {
    Cow::Borrowed(prompt)
} else {
    // Only clone when necessary
    Cow::Owned(prompt.clone().with_additional_items(missing_calls))
}
```

Each unnecessary operation compounds to create performance bottlenecks. Regularly review your code for these patterns and refactor when identified.