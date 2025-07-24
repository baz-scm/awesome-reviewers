---
title: Validate boundary conditions
description: Ensure algorithms handle boundary conditions and edge cases correctly
  by adding explicit validation for all input ranges. Special attention should be
  paid to index calculations, offset arithmetic, and memory management operations,
  as these are common sources of subtle bugs that only manifest in edge cases.
repository: rust-lang/rust
label: Algorithms
language: Rust
comments_count: 16
repository_stars: 105254
---

Ensure algorithms handle boundary conditions and edge cases correctly by adding explicit validation for all input ranges. Special attention should be paid to index calculations, offset arithmetic, and memory management operations, as these are common sources of subtle bugs that only manifest in edge cases.

When implementing algorithms:

1. Add explicit assertions or range checks for numerical bounds:
```rust
// Add safety check for numerical bounds
if let Some(ver) = ver {
    // Ensure version index doesn't conflict with special flags
    assert!(ver + 2 < VERSYM_HIDDEN);
    elf::VERSYM_HIDDEN | (2 + ver as u16)
}
```

2. Validate offset and length calculations to prevent overflows or out-of-bounds access:
```rust
// Use correct length calculation (not offset + length)
(inner_prov.alloc_id(), offset.bytes(), len)
```

3. For memory-related operations, handle special cases like indirect arguments or resource deallocation explicitly:
```rust
if tail {
    // Detect unsupported cases
    if has_indirect_args {
        bug!("musttail call with indirect arguments is not supported");
    }
    // Ensure proper ordering of operations
    bx.tail_call(fn_ty, fn_attrs, fn_abi, fn_ptr, llargs, self.funclet(fx), instance);
}
```

4. For complex dataflow analysis, verify that your algorithm handles uninitialized values, moved values, and aliasing correctly at all program points:
```rust
// Check storage liveness at every use location
if self.head_storage_to_check.contains(head) {
    self.maybe_storage_dead.seek_after_primary_effect(location);
    if self.maybe_storage_dead.get().contains(head) {
        self.storage_to_remove.insert(head);
    }
}
```

Thorough boundary condition validation prevents difficult-to-diagnose bugs and makes code more robust against unexpected inputs or state changes.