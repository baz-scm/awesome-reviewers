---
title: Avoid Hot-Path Deopts
description: 'When touching hot paths, optimize for allocation + JIT behavior + lifetime
  cleanup.


  Practical rules:

  - Don’t allocate closures in the common case. If a callback is only needed in a
  branch, create it inside that branch or use a reusable/module-level helper.'
repository: facebook/react#b10
label: Performance Optimization
language: JavaScript
comments_count: 9
repository_stars: 251894
---

When touching hot paths, optimize for allocation + JIT behavior + lifetime cleanup.

Practical rules:
- Don’t allocate closures in the common case. If a callback is only needed in a branch, create it inside that branch or use a reusable/module-level helper.
- Use cheap guards before calling heavy parsing/serialization logic (e.g., check a fast discriminant before entering a large function).
- Prefer engine-native primitives and stable singletons for conversions (avoid repeated chunk/allocation loops when a native decoder exists).
- Avoid constructs known to inhibit optimization in tight loops (e.g., `try/catch`/`try/finally` added for control flow). If you must use them, isolate the smallest possible scope via helper functions.
- Watch for memory retention: detach event listeners and sever strong reference chains when safe; otherwise you risk unbounded retention under load.
- Avoid per-iteration allocations in loops on hot paths (e.g., don’t create a `Set` just to detect duplicates when a small-array scan is cheaper).

Example pattern (closure + guard):
```js
// Bad: creates a closure in a condition-heavy area.
if (state.pending) {
  chunk.then(() => addDebugInfo(chunk));
} else {
  addDebugInfo(chunk);
}

// Better: add debug info without closure in the common case,
// and only allocate a callback in the pending branch.
function addDebugInfoForChunk(chunk) {
  // ...
}
if (chunk.status === 'pending' || chunk.status === 'blocked') {
  const cb = () => addDebugInfoForChunk(chunk);
  chunk.then(cb, cb);
} else {
  addDebugInfoForChunk(chunk);
}
```

Always verify with targeted benchmarks/profiling when behavior depends on JIT or GC (especially for serialization, streaming, and abort/cancellation paths).