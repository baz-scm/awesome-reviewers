---
title: Maintain focused module structure
description: Keep modules focused and well-organized by grouping related functionality
  together and splitting large files into logical submodules. Each file should have
  a clear, single responsibility. When a file grows too large or handles multiple
  concerns, consider breaking it into smaller, more focused modules.
repository: astral-sh/ruff
label: Code Style
language: Rust
comments_count: 4
repository_stars: 40619
---

Keep modules focused and well-organized by grouping related functionality together and splitting large files into logical submodules. Each file should have a clear, single responsibility. When a file grows too large or handles multiple concerns, consider breaking it into smaller, more focused modules.

For example, instead of:
```rust
// types.rs (large file with mixed concerns)
pub(crate) trait VarianceInferable<'db>: Sized {
    // ... variance-related code
}

pub(crate) struct TypeVarInstance<'db> {
    // ... type variable code
}
```

Prefer:
```rust
// types/variance.rs
pub(crate) trait VarianceInferable<'db>: Sized {
    // ... variance-related code
}

// types/type_var.rs
pub(crate) struct TypeVarInstance<'db> {
    // ... type variable code
}
```

Key guidelines:
- Keep files focused on a single responsibility or closely related set of functionality
- Use submodules to organize related code (e.g., types/variance.rs, types/type_var.rs)
- Consider splitting a file when it becomes difficult to navigate or understand as a whole
- Group related functionality together in the same module
- Use clear module names that reflect their contents