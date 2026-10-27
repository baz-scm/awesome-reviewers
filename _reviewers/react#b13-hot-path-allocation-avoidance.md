---
title: Hot-Path Allocation Avoidance
description: In performance-critical code, avoid adding work that creates allocations,
  closures, temporary objects/arrays, or deoptimizing patterns. Prefer native/engine-optimized
  primitives (and stable module-scope singletons) over manual chunking/transforms,
  and ensure you don’t accidentally retain data that prevents GC.
repository: facebook/react#b13
label: Performance Optimization
language: JavaScript
comments_count: 6
repository_stars: 251894
---

In performance-critical code, avoid adding work that creates allocations, closures, temporary objects/arrays, or deoptimizing patterns. Prefer native/engine-optimized primitives (and stable module-scope singletons) over manual chunking/transforms, and ensure you don’t accidentally retain data that prevents GC.

Apply this as a checklist:
- **Hoist and reuse**: move expensive helpers/state to module scope; don’t recreate regex/functions/objects per render/iteration.
- **Avoid closure churn**: don’t allocate `bind`/closures unless the slow/required branch is actually taken.
- **Avoid allocation-heavy manual transforms**: don’t use `Function.prototype.apply` on large arrays or repeated `subarray/slice` in loops when a native API exists.
- **Avoid deopt/invalidation triggers** in hot paths: avoid `try/finally` in tight render loops when not necessary; avoid layout reads like `getBoundingClientRect()` that can force layout.
- **Avoid GC retention**: sever strong reference chains when async/stream lifetimes end; don’t capture/retain stack data in long-lived abort paths.

Example: avoid chunked byte→string via `apply`, and use a singleton native decoder instead.
```js
// module scope
const latin1Decoder = new TextDecoder('latin1');

export function binaryToComparableString(view) {
  // Native path: fast and avoids chunk loops/arg-array limits
  return latin1Decoder.decode(new Uint8Array(view.buffer, view.byteOffset, view.byteLength));
}
```

Example: avoid closure creation in a hot-path when only needed in one branch.
```js
function maybeAddDebug(chunk, addDebugInfo) {
  if (chunk.status === PENDING || chunk.status === BLOCKED) {
    // allocate closure only when needed
    const bound = addDebugInfo.bind(null, chunk);
    chunk.then(bound, bound);
  } else {
    addDebugInfo(chunk);
  }
}
```

Rule of thumb: if you’re changing code inside a loop, render/commit, serialization, streaming, or async abort/completion handling—assume it’s hot and follow the checklist, then back it with a targeted benchmark/heap A-B when applicable.