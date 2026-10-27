---
title: Hot Path Allocation Rules
description: 'In performance-critical code, structure changes to avoid hidden deopts
  and avoidable allocations/GC pressure. Practical rules:


  - Avoid creating closures/functions inside hot branches/loops unless the deferred
  branch truly needs them; hoist shared helpers and only allocate the closure in the
  conditional path.'
repository: facebook/react#b17
label: Performance Optimization
language: JavaScript
comments_count: 11
repository_stars: 251891
---

In performance-critical code, structure changes to avoid hidden deopts and avoidable allocations/GC pressure. Practical rules:

- Avoid creating closures/functions inside hot branches/loops unless the deferred branch truly needs them; hoist shared helpers and only allocate the closure in the conditional path.
- Avoid introducing `try/catch` or `try/finally` in hot functions (it can inhibit optimization); if needed, isolate the minimal call behind a smaller wrapper.
- Avoid recursion in hot control flow when state checks can prevent deep call chains.
- Prefer native/platform primitives and singletons over manual chunking (e.g., use `TextDecoder` rather than `String.fromCharCode.apply` loops).
- Keep DOM reads from causing layout flushes (avoid `getBoundingClientRect` in render/measurement hot paths unless you’ve proven it’s safe).
- Avoid per-pass allocations in frequently-called render/commit loops; use cheap checks when possible, and sever long-lived strong reference chains so GC can reclaim memory.

Example (hoist helper; allocate closure only when needed):

```js
// Instead of allocating a closure on every call:
// chunk.then(() => addDebugInfo(chunk));

function addDebugInfoForChunk(chunk, awaitedInfo) {
  chunk._debugInfo.push(awaitedInfo);
}

function maybeAddDebugInfo(responseChunk, awaitedInfo, status) {
  if (status === 'PENDING' || status === 'BLOCKED') {
    // Allocate closure only for the deferred branch.
    const bound = addDebugInfoForChunk.bind(null, responseChunk, awaitedInfo);
    responseChunk.then(bound, bound);
  } else {
    addDebugInfoForChunk(responseChunk, awaitedInfo);
  }
}
```

Apply these standards especially in serialization/deserialization, rendering/commit traversal, devtools sampling/search, and any code that runs per element/node or per streamed chunk.