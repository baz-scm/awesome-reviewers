---
title: Clear helpful error messages
description: 'Create user-friendly error messages that guide developers toward solutions.
  Error messages should:

  1. Include the problematic value in the message

  2. Provide clear suggestions for fixing the issue'
repository: rust-lang/rust
label: Error Handling
language: Rust
comments_count: 6
repository_stars: 105254
---

Create user-friendly error messages that guide developers toward solutions. Error messages should:
1. Include the problematic value in the message
2. Provide clear suggestions for fixing the issue
3. Avoid duplicate errors for the same problem
4. Use help/note sections for additional context

Example:
```rust
// Instead of:
early_dcx.early_warn("option `-o` has no space between flag name and value");

// Do this:
early_dcx.early_warn(
    "option `-o` has no space between flag name and value, which can be confusing"
);
early_dcx.early_help(
    format!("insert a space between `-o` and `{name}` if this is intentional: `-o {name}`")
);
```

The error message should clearly identify the issue, show the problematic value, and provide actionable guidance for resolution. Use help/note sections to separate the error description from suggestions and additional context.