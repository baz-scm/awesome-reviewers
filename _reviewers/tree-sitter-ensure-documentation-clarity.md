---
title: Ensure documentation clarity
description: Documentation should be clear, accurate, and provide meaningful information
  to users. Avoid misleading descriptions, template text that doesn't add value, and
  unclear explanations that leave users confused about functionality.
repository: tree-sitter/tree-sitter
label: Documentation
language: Rust
comments_count: 5
repository_stars: 21799
---

Documentation should be clear, accurate, and provide meaningful information to users. Avoid misleading descriptions, template text that doesn't add value, and unclear explanations that leave users confused about functionality.

Key practices:
- Use precise terminology (prefer "display" over "print" for output operations)
- Ensure comments accurately describe what code actually does
- Remove template documentation that provides no useful information
- Include clear explanations of behavior, especially for complex or non-obvious functionality
- Add examples or clarifying details when the purpose or usage isn't immediately obvious

Example of unclear vs clear documentation:
```rust
// Unclear - misleading about actual behavior
/// Don't force rebuild the parser when `--grammar_path` is specified

// Clear - accurately describes the relationship
/// `--grammar_path` implies force rebuild
```

Documentation should help users understand not just what something does, but how and when to use it effectively.