---
title: consistent command flag design
description: Design command-line interfaces with consistent flag semantics and leverage
  framework features for validation. Avoid ambiguous syntax that can be interpreted
  multiple ways, use explicit conflict declarations instead of manual validation,
  and ensure flag combinations have clear, predictable behavior.
repository: jj-vcs/jj
label: API
language: Rust
comments_count: 11
repository_stars: 21171
---

Design command-line interfaces with consistent flag semantics and leverage framework features for validation. Avoid ambiguous syntax that can be interpreted multiple ways, use explicit conflict declarations instead of manual validation, and ensure flag combinations have clear, predictable behavior.

Key principles:
- Use clap's built-in `conflicts_with` instead of manual validation: `#[arg(long, conflicts_with = "other_flag")]`
- Separate command and arguments for better help messages: prefer `command: String, args: Vec<String>` over `command: Vec<String>`
- Avoid ambiguous syntax like accepting both "rs" and ".rs" for the same meaning
- Define clear semantics for flag combinations (intersection vs union behavior)
- Use exhaustive pattern matching for validation to prevent logic drift

Example of good flag design:
```rust
#[derive(clap::Args)]
struct Args {
    #[arg(long, conflicts_with = "push")]
    fetch: bool,
    
    #[arg(long, conflicts_with = "fetch")]  
    push: bool,
    
    // Clear semantics: when neither specified, both are true
    // When one specified, only that one is true
}
```

This ensures users can predict behavior and reduces maintenance burden by leveraging framework validation.