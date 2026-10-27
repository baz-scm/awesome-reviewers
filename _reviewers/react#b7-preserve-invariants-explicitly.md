---
title: Preserve Invariants Explicitly
description: When implementing transformation logic in an IR/compiler pipeline, ensure
  critical invariants are preserved end-to-end and that semantically distinct states
  are represented explicitly.
repository: facebook/react#b7
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 251888
---

When implementing transformation logic in an IR/compiler pipeline, ensure critical invariants are preserved end-to-end and that semantically distinct states are represented explicitly.

Apply this rule:
1) Preserve real data or make absence explicit
- For source locations/ranges: never silently propagate placeholder offsets. In conversion/build steps, either carry the real offset fields from the originating node, or explicitly clear/omit offset data when it’s not valid.
- Add regression tests for edge cases (shifted/absent offsets, colliding ranges, nested bindings).

2) Encode semantic categories with explicit variants
- For local-vs-context (or similar) distinctions: prefer dedicated enum variants (e.g., `PrefixUpdateLocal`/`PrefixUpdateContext`) instead of boolean flags (e.g., `is_context`). This prevents incorrect matches and eliminates fragile conditionals.

Example pattern (explicit variants instead of flags):
```rust
pub enum PrefixUpdate {
    PrefixUpdateLocal { /* ... */ },
    PrefixUpdateContext { /* ... */ },
}

// Downstream code matches directly on meaning.
match update {
    PrefixUpdate::PrefixUpdateLocal { .. } => { /* local logic */ }
    PrefixUpdate::PrefixUpdateContext { .. } => { /* context logic */ }
}
```

These practices reduce subtle correctness bugs in algorithmic transformations by making state unambiguous and invariants testable.