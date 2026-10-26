---
title: 'Performance: avoid allocations'
description: In performance-critical code, assume every extra allocation (closures,
  per-call helper functions, spread/copy, large temporary arrays) can trigger GC pressure,
  JIT deopts, or even stack overflows—and ensure lifecycle cleanup so listeners don’t
  retain large object graphs.
repository: facebook/react#b1
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 251878
---

In performance-critical code, assume every extra allocation (closures, per-call helper functions, spread/copy, large temporary arrays) can trigger GC pressure, JIT deopts, or even stack overflows—and ensure lifecycle cleanup so listeners don’t retain large object graphs.

Guidelines:
- Avoid closure capture in hot paths: create callbacks via `.bind` or module-level helpers; don’t allocate closures unless the condition requires them.
- Prefer native, engine-optimized primitives for data transforms (e.g., `TextDecoder`) and use bounded strategies that avoid exceeding engine limits.
- Don’t rely on long-lived listeners/reference chains: detach abort/event listeners and sever unnecessary strong links so GC can reclaim request graphs.
- Avoid recursion in fan-out/loop-heavy logic; prefer explicit state checks and iterative control flow.

Example (closure allocated only when needed):
```js
function resolveChunkDebugInfo(chunk, streamState) {
  if (__DEV__ && enableAsyncDebugInfo) {
    const debugInfoEntry = {awaited: streamState._debugInfo};

    const addDebugInfo = () => {
      // ... use chunk + debugInfoEntry ...
    };

    if (chunk.status === PENDING || chunk.status === BLOCKED) {
      // Allocate the bound callback only in the pending branch.
      const boundAdd = addDebugInfo.bind(null);
      chunk.then(boundAdd, boundAdd);
    } else {
      addDebugInfo();
    }
  }
}
```

Example (detach abort listener to avoid retention):
```js
export function attachAbortSignal(request, signal) {
  function listener() {
    detach();
    abort(request, signal.reason);
  }
  function detach() {
    request.detachAbortSignal = null;
    signal.removeEventListener('abort', listener);
  }
  request.detachAbortSignal = detach;
  signal.addEventListener('abort', listener);
}
```

Apply this as a review rubric for any hot serialization/streaming path, render/commit loop, or async/lifecycle hook: if it creates closures/arrays/objects per call, prove it’s necessary—or refactor to reuse, gate allocation, or move work to native bounded paths, and ensure cleanup prevents retention leaks.