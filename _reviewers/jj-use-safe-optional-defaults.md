---
title: Use safe optional defaults
description: When working with optional values, prefer safe extraction methods that
  provide defaults rather than methods that can panic. Use `unwrap_or()`, `unwrap_or_default()`,
  or `unwrap_or_else()` instead of `unwrap()` to handle `None` cases gracefully.
repository: jj-vcs/jj
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 21171
---

When working with optional values, prefer safe extraction methods that provide defaults rather than methods that can panic. Use `unwrap_or()`, `unwrap_or_default()`, or `unwrap_or_else()` instead of `unwrap()` to handle `None` cases gracefully.

This pattern prevents runtime panics and makes code more robust by explicitly handling the absence of values. It's particularly important when dealing with configuration values, map lookups, or any operation that might not return a result.

Examples of good patterns:
```rust
// Instead of potentially panicking
let executable = file.executable.unwrap();

// Use safe defaults
let executable = file.executable.unwrap_or(false);

// For common defaults
let config = maybe_read_to_string(&path)?.unwrap_or_default();

// For map lookups
let parent = old_to_new.get(p.id()).unwrap_or(&p);
```

This approach makes the code's behavior predictable and prevents unexpected crashes when optional values are absent, while clearly documenting the intended fallback behavior.