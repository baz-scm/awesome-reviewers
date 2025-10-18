---
title: Use type-specific variable names
description: Use distinct variable names that reflect their types to avoid confusion
  and make code intent clearer. Avoid reusing the same variable name for different
  types within the same scope or related functions.
repository: jj-vcs/jj
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 21171
---

Use distinct variable names that reflect their types to avoid confusion and make code intent clearer. Avoid reusing the same variable name for different types within the same scope or related functions.

This prevents confusion when tracking values as they pass through functions and makes the code more maintainable. When variables of different types serve similar purposes, use descriptive suffixes or prefixes that indicate the type.

Example from the codebase:
```rust
// Bad: Same name for different types
let executable: bool = file.is_executable();
let executable: FileExecutableFlag = FileExecutableFlag::from(executable);

// Good: Type-specific names
let executable: bool = file.is_executable();
let exec_bit: ExecBit = ExecBit::from(executable);
```

Other examples:
- Use `handle` instead of `val` for `same_file::Handle` objects
- Use `remote_branch` instead of ambiguous `origin` for branch parameters
- Distinguish between `remote_url` and `push_url` when both are URLs but serve different purposes

This practice is especially important in functions that transform data between types or when working with similar concepts at different abstraction levels.