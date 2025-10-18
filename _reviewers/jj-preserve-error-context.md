---
title: preserve error context
description: When handling errors, preserve the original error context and avoid exposing
  internal representations to users. Use `IoResultExt::context()` to attach meaningful
  path information to I/O errors, and maintain error source chains using `.with_source()`
  or similar mechanisms.
repository: jj-vcs/jj
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 21171
---

When handling errors, preserve the original error context and avoid exposing internal representations to users. Use `IoResultExt::context()` to attach meaningful path information to I/O errors, and maintain error source chains using `.with_source()` or similar mechanisms.

For user-facing error messages, avoid displaying internal data structures that users cannot understand. Instead, provide clear, actionable error descriptions.

Example of good error context preservation:
```rust
// Good: Attach path context to I/O errors
std::fs::write(&jj_gitignore_path, "/*\n")
    .context(&jj_gitignore_path)?;

// Good: Preserve error source chain  
TemplateParseError::expression(message, span).with_source(err)

// Bad: Expose internal representation to user
format!("The given revset '{:?}' was expected to have {} elements", set, count)

// Good: User-friendly message
format!("revset that was expected to have {} revision had {} revisions", expected, actual)
```

This approach ensures that developers get sufficient debugging information while users receive comprehensible error messages. The error context helps with troubleshooting without overwhelming end users with implementation details.