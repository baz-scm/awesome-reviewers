---
title: Atomic Contracts Enforcement
description: 'Define and enforce atomicity as an explicit contract: if correctness
  depends on thread/writer invariants, encode it in the API name/docs and validate
  it at usage sites; if a value can be concurrently updated, read/write it exclusively
  via atomic operations (no non-atomic peeking into parts of an atomic container).'
repository: redis/redis
label: Concurrency
language: Other
comments_count: 4
repository_stars: 74261
---

Define and enforce atomicity as an explicit contract: if correctness depends on thread/writer invariants, encode it in the API name/docs and validate it at usage sites; if a value can be concurrently updated, read/write it exclusively via atomic operations (no non-atomic peeking into parts of an atomic container).

Practical rules:
1) Single-writer “atomic” helpers
- If an operation is implemented with load+add+store (not true RMW), it must be correct only under a strict single-writer rule.
- Make that rule unmissable in the name and comment (e.g., `...SingleWriter...`), and ensure no other thread can ever update the same variable.

2) Packed atomic bitfields
- Treat the entire storage (e.g., `atomic_flags_refcount`) as atomic.
- If only some bits are intended to be immutable after init, state that assumption explicitly and ensure code never violates it.
- All reads of the atomic container must use `atomicGet` (or equivalent) before masking/shifting; don’t read the underlying integer non-atomically from another thread.

3) Document IO-thread vs main-thread invariants
- When refcounts/pointers are updated in different thread phases, comments must explain what is safe to update when, and why—field names should reflect semantics (e.g., “current node” vs “start node”).

Example (atomic-packed refcount access):
```c
#define OBJ_REFCOUNT_MASK ((1U << OBJ_REFCOUNT_BITS) - 1)
#define OBJ_EXPIRABLE_BIT 30
#define OBJ_ISKVOBJ_BIT 31

static inline unsigned robj_refcount(const robj *o) {
    uint32_t v;
    atomicGet(o->atomic_flags_refcount, v); // must be atomic
    return v & OBJ_REFCOUNT_MASK;
}

static inline unsigned robj_expirable(const robj *o) {
    uint32_t v;
    atomicGet(o->atomic_flags_refcount, v); // must be atomic
    return (v >> OBJ_EXPIRABLE_BIT) & 1;
}
```

If you can’t clearly state the invariants and make every concurrent access atomic-safe, redesign the ownership model or synchronization rather than relying on “it never races” assumptions.