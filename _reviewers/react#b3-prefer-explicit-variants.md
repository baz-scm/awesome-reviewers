---
title: Prefer explicit variants
description: When a field’s value represents a semantic role or identity (e.g., computed
  vs non-computed, local vs context), do not encode it with a boolean flag in an otherwise
  generic instruction. Instead, use existing (or introduce new) explicitly named variants/types
  so the name itself carries meaning and passes can match directly.
repository: facebook/react#b3
label: Naming Conventions
language: Rust
comments_count: 2
repository_stars: 251883
---

When a field’s value represents a semantic role or identity (e.g., computed vs non-computed, local vs context), do not encode it with a boolean flag in an otherwise generic instruction. Instead, use existing (or introduce new) explicitly named variants/types so the name itself carries meaning and passes can match directly.

Apply this rule by:
- If the HIR already has dedicated variants (e.g., `ComputedStore`/`ComputedLoad`), reuse them rather than adding `computed: bool`.
- If an operation differs by role (e.g., local vs context), add explicit variants instead of `is_context: bool` (e.g., `PrefixUpdateLocal` / `PrefixUpdateContext`, `PostfixUpdateLocal` / `PostfixUpdateContext`).
- Avoid downstream logic that branches on the flag; match on the named variant.

Example (flag → explicit variants):
```rust
// Avoid:
// PrefixUpdate { is_context: bool, ... }

// Prefer:
enum InstructionValue {
  PrefixUpdateLocal { /* ... */ },
  PrefixUpdateContext { /* ... */ },
  PostfixUpdateLocal { /* ... */ },
  PostfixUpdateContext { /* ... */ },
}

// Then passes match directly on the variant rather than checking a flag.
```