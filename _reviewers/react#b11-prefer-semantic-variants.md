---
title: Prefer semantic variants
description: When a boolean flag exists solely to distinguish different semantic instruction
  kinds (e.g., computed vs non-computed, local vs context), prefer explicit, semantically-named
  enum variants instead of `bool` fields.
repository: facebook/react#b11
label: Naming Conventions
language: Rust
comments_count: 2
repository_stars: 251894
---

When a boolean flag exists solely to distinguish different semantic instruction kinds (e.g., computed vs non-computed, local vs context), prefer explicit, semantically-named enum variants instead of `bool` fields.

Why: boolean flags make identifiers less self-describing and force downstream logic to branch on meaning; explicit variants improve naming clarity and pattern matching consistency.

Do
- Use/introduce distinct variants with clear names that encode the meaning.
- Update passes to match the variants directly.

Avoid
- Adding fields like `computed: bool` or `is_context: bool` when the behavior corresponds to an already-defined (or easily defined) concept.

Example pattern (modeled after the discussion outcomes):
```rust
enum PrefixUpdate {
    PrefixUpdateLocal( /* ... */ ),
    PrefixUpdateContext( /* ... */ ),
}
// instead of: PrefixUpdate { ..., is_context: bool }
```
And for computed operations:
```rust
enum InstructionValue {
    ComputedStore { /* ... */ },
    ComputedLoad { /* ... */ },
    // instead of: PropertyStore { /* ... */ computed: bool }
}
```