---
title: Benchmark hot-path regressions
description: When adding bookkeeping for correctness or edge cases (deduplication,
  debug stats, extra tracking structures), make sure the common/fast path doesn't
  pay for work it doesn't need. Defer allocations, extra passes, or per-call checks
  until they're actually required, and fall back to a cheap path when the condition
  that triggers the extra cost is absent or...
repository: python/cpython
label: Performance Optimization
language: C
comments_count: 4
repository_stars: 77696
---

When adding bookkeeping for correctness or edge cases (deduplication, debug stats, extra tracking structures), make sure the common/fast path doesn't pay for work it doesn't need. Defer allocations, extra passes, or per-call checks until they're actually required, and fall back to a cheap path when the condition that triggers the extra cost is absent or rare.

Before merging such a change, measure both the previously-fast case and the newly-added case with realistic micro-benchmarks (median over multiple runs, release build) to confirm there's no unacceptable regression. If a benchmark reveals a regression (e.g. allocating a dict/set on every call even when no duplicates/empty slots exist, or iterating a list twice just to get a count), redesign the algorithm so the expensive work is only triggered by the actual condition, not unconditionally.

For example, instead of always allocating a tracking set/dict for every frame to deduplicate local names:
```c
// Bad: always pay the cost, even when no duplicates exist
PyObject *seen = PySet_New(NULL);
for (...) {
    // dedup logic touches "seen" on every slot, every call
}
```
use a cached/lazy marker that skips the extra data structure entirely unless duplicates are known or suspected:
```c
// Good: only allocate/iterate the extra structure when needed
if (FT_ATOMIC_LOAD_CHAR_RELAXED(co->_co_localsplus_dedup) == DEDUP_UNIQUE) {
    // skip tracking entirely - fast path
} else {
    // only now pay for the dict/set and walk
}
```

Similarly, avoid doing two full passes over the same data when one pass can produce both results (e.g., compute a count while iterating for debug output instead of iterating once to print and once again to count). Treat any added per-call overhead as a performance regression candidate until proven negligible by measurement.