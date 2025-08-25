---
title: Document non-obvious code
description: Add clear documentation for code elements that aren't immediately self-explanatory
  to improve readability and maintainability. This includes replacing magic numbers
  with named constants, adding explanatory comments for complex types, and ensuring
  documentation remains consistent and synchronized across different contexts.
repository: block/goose
label: Documentation
language: Rust
comments_count: 3
repository_stars: 19037
---

Add clear documentation for code elements that aren't immediately self-explanatory to improve readability and maintainability. This includes replacing magic numbers with named constants, adding explanatory comments for complex types, and ensuring documentation remains consistent and synchronized across different contexts.

Key practices:
- Replace magic numbers with documented constants: `const LINE_LIMIT: usize = 2000;` instead of using `2000` directly
- Document complex types with clear explanations of their behavior and purpose
- Keep documentation synchronized across platforms and contexts to avoid confusion
- Add inline comments that explain the "why" and "what" for non-obvious code constructs

Example for type documentation:
```rust
/// A message stream yields partial text content but complete tool calls, 
/// all within the Message object. So a message with text will contain 
/// potentially just a word of a longer response
pub type MessageStream = Pin<...>;
```

This practice helps new team members understand the codebase faster and reduces the cognitive load when reviewing or modifying code.