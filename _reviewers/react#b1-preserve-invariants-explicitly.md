---
title: Preserve invariants explicitly
description: 'Encode correctness-affecting state as explicit data (types/variants)
  and ensure invariants are preserved across each transformation step.


  Apply this when:'
repository: facebook/react#b1
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 251878
---

Encode correctness-affecting state as explicit data (types/variants) and ensure invariants are preserved across each transformation step.

Apply this when:
- Source-location fields must remain semantically consistent (e.g., real offsets vs derived indices). If some pipeline stage uses placeholder positions, downstream code must either replace them with the real offsets or explicitly clear/validate that the placeholder isn’t treated as real.
- Mode/context distinctions affect semantics. Prefer explicit enum variants over boolean flags, so the compiler can’t silently take the wrong path.

Example pattern (explicit variants over flags):

```rust
// Avoid: PrefixUpdate { is_context: bool }
// Prefer:
enum PrefixUpdate {
    PrefixUpdateLocal { /* ... */ },
    PrefixUpdateContext { /* ... */ },
}
```

Example pattern (offset invariant):

- Ensure `start_offset` is sourced from the same “truth” as the rest of the location model. Don’t let placeholder `base.start` propagate as a real offset; either keep real offsets end-to-end or gate downstream logic when offsets are placeholders.