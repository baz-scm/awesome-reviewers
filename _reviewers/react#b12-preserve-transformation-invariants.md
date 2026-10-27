---
title: Preserve transformation invariants
description: 'When implementing compiler/data transformations (e.g., AST→HIR lowering,
  outlining, or instruction lowering), treat semantic fields as invariants: preserve
  the authoritative values across every pipeline path, and model semantic alternatives
  explicitly (not via ambiguous flags). Add regression tests for edge cases where
  inputs may contain placeholders,...'
repository: facebook/react#b12
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 251896
---

When implementing compiler/data transformations (e.g., AST→HIR lowering, outlining, or instruction lowering), treat semantic fields as invariants: preserve the authoritative values across every pipeline path, and model semantic alternatives explicitly (not via ambiguous flags). Add regression tests for edge cases where inputs may contain placeholders, shifted ranges, collisions, or missing data.

Apply this rule:
- Source-location/offsets: ensure every transformation path either (a) carries the real offset from the authoritative field, or (b) cleanly marks it as absent/invalid. Don’t let placeholder positions silently become “real” offsets.
- IR/instruction semantics: represent distinct meaning as separate enum variants (e.g., Local vs Context) rather than `bool is_context`, and make backends match by variant.
- Lock correctness with tests covering shifted/absent/colliding ranges and nested bindings.

Example (replace boolean flag with explicit variants):
```rust
// Prefer explicit variants over flags
pub enum PrefixUpdate {
    PrefixUpdateLocal { /* ... */ },
    PrefixUpdateContext { /* ... */ },
}

// Avoid:
// PrefixUpdate { is_context: bool, /* ... */ }
```

This reduces correctness bugs caused by invariant drift and improves maintainability by preventing “implicit” semantic meanings encoded in flags.