---
title: Justify and invalidate caches
description: 'When adding a cache (e.g., memoizing a lookup such as resolving an exception
  class to its registered handler), two things must be verified before merging:'
repository: pallets/flask#x
label: Caching
language: Python
comments_count: 4
repository_stars: 75163
---

When adding a cache (e.g., memoizing a lookup such as resolving an exception class to its registered handler), two things must be verified before merging:

1. **Invalidation correctness.** The cache key and population logic must correctly reflect the mutability of the underlying data. If the cached relationship can change at runtime (e.g., a new, more specific handler is registered after a lookup for a subclass has already been cached), the cache must be invalidated for all affected keys, not just populated once and left stale. For example, caching `d[exc_class] = handler` without clearing superclass entries on new registrations can cause a previously cached subclass lookup to keep returning an old, less-specific handler even after a more specific one is added:

```python
@app.errorhandler(OSError)
def handle_os_error(e): ...

# ConnectionAbortedError raised -> cached as handle_os_error

@app.errorhandler(ConnectionError)
def handle_connection_error(e): ...

# ConnectionAbortedError raised again -> still returns stale cached handle_os_error
```
If the system guarantees an invariant that makes invalidation unnecessary (e.g., "routes/handlers cannot be registered after app start"), that invariant must be explicitly documented and enforced, not just assumed.

2. **Performance justification.** Caching adds complexity and potential for subtle bugs, so its inclusion should be justified by a demonstrated performance benefit (profiling/benchmark data), not merely by arguing that it "doesn't cause problems." The burden of proof is on showing the cache meaningfully improves performance, not on showing its absence is harmful. Avoid introducing speculative optimizations (e.g., precomputing all possible subclasses ahead of time) that are either infeasible (open class hierarchies) or unproven in value.

In short: before caching, confirm (a) how and when invalidation happens relative to data mutations, and (b) that the caching is backed by evidence of real performance gain.</description>
</invoke>
