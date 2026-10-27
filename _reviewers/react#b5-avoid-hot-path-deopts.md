---
title: Avoid Hot-Path Deopts
description: 'In performance-critical code paths, avoid patterns that trigger deoptimization,
  deep call stacks, or unnecessary allocations.


  Apply these rules:

  - **Hoist or bind instead of allocating closures** in hot logic paths (e.g., event
  handlers/cleanup functions, serialization helpers).'
repository: facebook/react#b5
label: Performance Optimization
language: JavaScript
comments_count: 6
repository_stars: 251886
---

In performance-critical code paths, avoid patterns that trigger deoptimization, deep call stacks, or unnecessary allocations.

Apply these rules:
- **Hoist or bind instead of allocating closures** in hot logic paths (e.g., event handlers/cleanup functions, serialization helpers).
- **Avoid adding `try/finally`** around frequently executed render/serialization work if it blocks optimization; restructure control flow to keep the hot function optimizer-friendly.
- **Avoid recursion** for fanout-driven work (e.g., many listeners/references); prefer iterative “check state then dispatch” logic.
- **Minimize allocations in passes** that run often (avoid creating Sets/objects/spreads per level/iteration when common-case work needs none).
- **Prefer engine-native APIs and module-level singletons** for heavy transforms instead of manual chunk loops that allocate intermediate arrays.

Example (recursion → state-check dispatch):
```js
// Prefer: check status and dispatch without recursive re-entry.
function wakeIfReady(chunk) {
  if (chunk.status === 'initialized') {
    wakeChunk(chunk);
  } else if (chunk.status === 'errored') {
    rejectChunk(chunk, chunk.error);
  }
  // else: leave pending
}
```

Example (native transform singleton):
```js
// Prefer a module-level decoder over manual chunk+apply loops.
const latin1Decoder = new TextDecoder('latin1');
function bytesToComparable(bytes) {
  return latin1Decoder.decode(bytes);
}
```

When you must change behavior, keep perf-risky changes isolated and back them with targeted benchmarks/profiling for the affected path.