---
title: Name for semantic meaning
description: Choose names that clearly convey the semantic meaning and purpose of
  the identifier, rather than using clever or ambiguous names. Names should be explicit
  and descriptive enough that their purpose is immediately clear to readers.
repository: rust-lang/rust
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 105254
---

Choose names that clearly convey the semantic meaning and purpose of the identifier, rather than using clever or ambiguous names. Names should be explicit and descriptive enough that their purpose is immediately clear to readers.

Key guidelines:
- Use explicit descriptive names over clever/compact alternatives
- Include relevant type or role information in the name
- Avoid ambiguous names when similar concepts are in scope

Example:
```rust
// Less clear:
impl LintStoreMarker for Store { }
let id = trait_pred.self_ty();

// More clear:
impl DynLintStore for Store { }
let type_id = trait_pred.self_ty();
```

This approach makes code more maintainable and self-documenting by reducing cognitive load on readers. When multiple similar concepts are in scope, use more specific names to distinguish their roles.