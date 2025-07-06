---
title: Prefer explicit over concise
description: Choose explicit and unambiguous names over concise but unclear ones.
  When a method, type, or variable has a specific behavior or purpose, the name should
  clearly communicate that, even if it results in longer names.
repository: tokio-rs/tokio
label: Naming Conventions
language: Rust
comments_count: 6
repository_stars: 28989
---

Choose explicit and unambiguous names over concise but unclear ones. When a method, type, or variable has a specific behavior or purpose, the name should clearly communicate that, even if it results in longer names.

For example:
- Use `AsyncFdTryNewError` instead of a generic error name to clearly indicate its purpose
- Choose `AbortOnDropHandle` over shorter alternatives to communicate the type's behavior
- Prefer `sender_strong_count()` over `strong_count()` when the context requires clarity about which entity's count is being returned
- Use `notify_one_last_in()` rather than `notify_one_lifo()` to make the behavior more obvious
- Name a method `copy_bidirectional_with_sizes()` instead of `copy_bidirectional_with_size()` when it takes multiple size parameters
- Choose `clone_inner()` over `clone()` to avoid confusion with the standard `Clone` trait implementation

While conciseness has value, clarity and explicitness should take precedence when there's potential for ambiguity or confusion. This principle applies to all identifiers including variables, methods, functions, types, and modules.