---
title: Correct Fast-Path Semantics
description: When implementing algorithmic optimizations (fast paths, binary search
  vs linear, prefetch/slot routing, realloc/compaction shortcuts), require *semantic
  correctness* and *invariant preservation* before performance.
repository: redis/redis
label: Algorithms
language: C
comments_count: 7
repository_stars: 74261
---

When implementing algorithmic optimizations (fast paths, binary search vs linear, prefetch/slot routing, realloc/compaction shortcuts), require *semantic correctness* and *invariant preservation* before performance.

Apply this standard:
- **Guard fast paths with exactness conditions** (range, precision, rounding model). If the proof/assumption doesn’t hold, **fall back** to the reference/slow path.
- **Match externally observable semantics exactly** (e.g., parse success vs failure, and `endptr`/“consumed input” behavior). Never accept partial parses just because a value (like `nan`) was detected.
- **Use overflow checks that match the actual arithmetic** (multiplication vs addition). Validate the intermediate that can overflow, not just a later result.
- **After possible realloc/relayout**, re-apply any derived indexes/maps that depend on the old address/layout (e.g., tree/rax nodes pointing at listpack memory).
- **Defer micro-optimizations** if correctness is the priority and the difference is unlikely to matter at RC time; choose the simpler correct algorithm first.

Example (parsing correctness guard):
```c
// Rule: only accept nan(...) if the parse consumed the expected characters.
if (parsed && isnan(result)) {
    if (endptr) *endptr = (char*)eptr;
    // But also ensure the parse covered the full grammar for the token.
    // If eptr != pend for an otherwise-invalid/partial nan(...), reject.
}
```

Example (overflow check matching operation):
```c
// If overflow risk is in multiplication, check multiplication, not addition.
if (emission_interval_us > LLONG_MAX / num_requests) {
    addReplyError(c, "overflow");
    return;
}
```