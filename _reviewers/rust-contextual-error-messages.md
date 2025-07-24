---
title: Contextual error messages
description: Error messages should provide specific context about the error and guide
  users toward solutions. When reporting syntax errors like mismatched delimiters,
  include both the location of the error and references to related code elements to
  help users quickly identify the problem.
repository: rust-lang/rust
label: Error Handling
language: Other
comments_count: 4
repository_stars: 105254
---

Error messages should provide specific context about the error and guide users toward solutions. When reporting syntax errors like mismatched delimiters, include both the location of the error and references to related code elements to help users quickly identify the problem.

For parser errors, prefer specific diagnostics over generic ones. Instead of vague messages like "mismatched closing delimiter", use more helpful guidance such as "missing open `(` for this delimiter" with clear indication of where both delimiters are located.

Example:
```
error: missing open `(` for a `)` delimiter
  --> file.rs:3:1
   |
LL | pub fn foo(x: i64) -> i64 {
   |                           - the last matched opening delimiter
LL |     x.abs)
   |          ^ missing open `(` for this delimiter
```

This approach helps users quickly understand the scope of the error and reduces debugging time by pinpointing both the error and its context. Remember that the goal of error messages is not just to report problems but to guide users toward solutions.