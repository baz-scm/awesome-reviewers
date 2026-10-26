---
title: Avoid Hot-Path Allocations
description: In performance-sensitive code, avoid creating new allocations (closures,
  temporary arrays/objects, subarrays/slices) and avoid patterns that trigger JIT/deopt.
  Prefer hoisted/module-scope helpers, native primitives, and deferred/memoized expensive
  work—while keeping correctness and memory safety guarantees.
repository: facebook/react#b2
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 251882
---

In performance-sensitive code, avoid creating new allocations (closures, temporary arrays/objects, subarrays/slices) and avoid patterns that trigger JIT/deopt. Prefer hoisted/module-scope helpers, native primitives, and deferred/memoized expensive work—while keeping correctness and memory safety guarantees.

Practical rules:
- **Don’t allocate closures in hot conditions**: create the closure only in the branch that needs it, or bind once with a hoisted helper.
- **Hoist helpers/data**: move repeated logic (e.g., `TextDecoder`, predicate helpers) to module scope so it’s reused and doesn’t recreate per call.
- **Prefer native/built-in conversions** over manual chunk loops that allocate frequently.
- **Defer expensive work** (search/tree walks) to transition/idle priority; memoize results and keep UI responsive.
- **Stabilize object shapes**: keep property sets/order consistent; don’t introduce optional properties late in a frequently executed path.
- **Avoid unnecessary passes in common cases**: check fast conditions before doing heavier loops/allocations.

Example (closure allocation only in the needed branch):
```js
function addDebugInfoEntry(entry) {
  return entry; // or push into an array, etc.
}

if (chunk.status === PENDING || chunk.status === BLOCKED) {
  // Only allocate the closure when we actually need to attach it.
  const handler = () => addDebugInfoEntry(debugInfo);
  chunk.then(handler, handler);
} else {
  addDebugInfoEntry(debugInfo);
}
```

Apply this standard when reviewing code that runs per chunk/frame/per node/per request, or that is known to show perf or memory issues under load.