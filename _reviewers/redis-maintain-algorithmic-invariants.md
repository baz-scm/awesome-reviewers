---
title: Maintain algorithmic invariants
description: When implementing algorithms that depend on “current state” (client context,
  cached slot/client, etc.) or on custom data structures (stack/heap modes), make
  the invariant explicit and ensure all computations are derived from the specific
  operand/object being processed—not from incidental outer execution context.
repository: redis/redis
label: Algorithms
language: Other
comments_count: 3
repository_stars: 74261
---

When implementing algorithms that depend on “current state” (client context, cached slot/client, etc.) or on custom data structures (stack/heap modes), make the invariant explicit and ensure all computations are derived from the specific operand/object being processed—not from incidental outer execution context.

Practical rules:
- Operand over incidental context: in nested execution (e.g., MULTI/EXEC where commands run while other client state is active), compute shard slot / routing from the key/channel argument itself and do not rely on cached “current_client”/slot.
- Encode ownership & storage mode: for DSs with multiple backing stores (stack vs heap), clearly define what is owned/freed, what is never freed, and when heap allocation happens.
- Allocation discipline: in Redis core, use Redis allocator wrappers (zmalloc/zrealloc/zfree), not libc allocation.
- Ergonomics that reduce misuse: prefer DS shapes that make correct usage easy (e.g., embed a small fixed buffer variant like SmallVector rather than forcing callers to manage extra stack buffers), and keep the API naming consistent with Redis style.

Example (stack-embedded “small vector” idea):
```c
// SmallVector-like: small fixed buffer embedded in the DS.
typedef struct vec {
    size_t size;
    size_t cap;
    void **data;
    void *small[VEC_DEFAULT_INITCAP];
} vec;

void vecInit(vec *v, size_t hint) {
    v->size = 0;
    if (hint <= VEC_DEFAULT_INITCAP) {
        v->data = v->small;
        v->cap = VEC_DEFAULT_INITCAP;
    } else {
        v->data = zmalloc(sizeof(void*) * hint);
        v->cap = hint;
    }
}

void vecDestroy(vec *v) {
    if (v->data != v->small) zfree(v->data);
}
```

Apply this mindset to both algorithmic routing decisions and DS implementations: correctness comes from invariants tied to the actual data being acted upon, and API/structure choices that prevent accidental reliance on stale execution-context or ambiguous ownership.