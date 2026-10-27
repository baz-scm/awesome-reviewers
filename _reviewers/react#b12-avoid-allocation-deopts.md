---
title: Avoid Allocation Deopts
description: 'In performance-critical code paths, minimize allocation/deoptimization
  risks: avoid per-call closures, keep object shapes stable, avoid patterns that inhibit
  JIT (e.g., new try blocks in hot code, layout-flushing DOM reads), and prefer engine-native
  primitives over JS-level chunk loops. When work can be deferred, defer it (and show
  pending UI) instead of...'
repository: facebook/react#b12
label: Performance Optimization
language: JavaScript
comments_count: 9
repository_stars: 251896
---

In performance-critical code paths, minimize allocation/deoptimization risks: avoid per-call closures, keep object shapes stable, avoid patterns that inhibit JIT (e.g., new try blocks in hot code, layout-flushing DOM reads), and prefer engine-native primitives over JS-level chunk loops. When work can be deferred, defer it (and show pending UI) instead of blocking.

Practical rules:
- Hoist reusable helpers to module scope; don’t allocate closures unless you must, and don’t allocate them outside a conditional.
- For hot call sites, restructure to remove runtime checks/branchy code that bloats the function; where needed, split into two code paths so the fast path stays simple.
- Avoid DOM layout flushes in render/streaming paths (e.g., don’t call getBoundingClientRect as a “should we flush?” probe).
- Replace JS chunk loops over large arrays with native APIs when correctness permits (and keep guarantees explicit).
- Avoid copying entire “tails” of large arrays for continuation tasks when an index-based approach can reduce churn.
- If expensive traversal/search is user-triggered, derive results from deferred state and gate with a spinner rather than doing synchronous work on every keystroke.

Example (closure hoisting in a hot branch):
```js
// module scope
function addDebugInfoEntry(chunk, awaitedDebugInfo) {
  // mutate/push debug info using precomputed values
}

function resolveDebugInfo(chunk, streamState) {
  const awaited = streamState._debugInfo;
  if (chunk.status === 'PENDING' || chunk.status === 'BLOCKED') {
    // only allocate a closure in the delayed branch
    const bound = () => addDebugInfoEntry(chunk, awaited);
    chunk.then(bound, bound);
  } else {
    addDebugInfoEntry(chunk, awaited);
  }
}
```

Example (native API vs JS chunking):
```js
// module scope
const textDecoderLatin1 = new TextDecoder('latin1');

export function binaryToComparableString(view) {
  // native decode avoids per-chunk apply/subarray allocation
  return textDecoderLatin1.decode(view);
}
```

Adopting these patterns reduces hidden-class churn, JIT deopts, backpressure jitter, and GC pressure—directly improving throughput and tail latency.