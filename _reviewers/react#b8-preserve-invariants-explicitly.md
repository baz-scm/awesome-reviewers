---
title: Preserve invariants explicitly
description: When transforming or transporting compiler data structures (e.g., source
  locations or HIR instructions), preserve the underlying invariants explicitly and
  avoid “implicit” or “flag-driven” semantics.
repository: facebook/react#b8
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 251889
---

When transforming or transporting compiler data structures (e.g., source locations or HIR instructions), preserve the underlying invariants explicitly and avoid “implicit” or “flag-driven” semantics.

Apply this in two ways:
1) Source-location conversions: Don’t assume fields derived from indices/placeholders are “real.” If the upstream pipeline may write placeholder positions, ensure your conversion either:
   - copies the true offset field only when it is genuinely available, or
   - clears/omits the offset field when it isn’t real.
   Also add regression tests for shifted/absent offsets, colliding ranges, and nested bindings.

2) Semantic distinctions in IR/HIR: Prefer explicit enum variants over boolean flags for semantic categories. Boolean flags tend to create scattered, non-exhaustive branching and make it easier to accidentally mix local/context behavior.

Example (variant-based, flag-free):
```rust
// Prefer explicit variants over a flag on a single variant.
pub enum InstructionValue {
    PrefixUpdateLocal { /* ... */ },
    PrefixUpdateContext { /* ... */ },
    PostfixUpdateLocal { /* ... */ },
    PostfixUpdateContext { /* ... */ },
}

// Then downstream can match directly without `is_context` checks.
```

Result: conversions remain correct across phases, and control flow stays exhaustive and consistent—reducing subtle regressions in both correctness (offsets) and maintainability (IR semantics).