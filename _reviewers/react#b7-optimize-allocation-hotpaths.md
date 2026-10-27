---
title: Optimize Allocation Hotpaths
description: 'When optimizing for performance, treat allocation/GC and engine/JIT
  stability as first-class concerns.


  **Do**

  - **Avoid unnecessary allocations in hot paths**: don’t create closures/objects/arrays
  unless the branch needs them; prefer hoisted helpers and stable call patterns.'
repository: facebook/react#b7
label: Performance Optimization
language: JavaScript
comments_count: 9
repository_stars: 251888
---

When optimizing for performance, treat allocation/GC and engine/JIT stability as first-class concerns.

**Do**
- **Avoid unnecessary allocations in hot paths**: don’t create closures/objects/arrays unless the branch needs them; prefer hoisted helpers and stable call patterns.
- **Keep object shapes stable**: inline object literals can introduce hidden-class churn; extract construction into helpers when shape/order stability matters.
- **Avoid optimizer blockers**: be wary of `try/catch` and extra runtime checks in performance-critical code; prefer isolation via separate functions or minimizing checks.
- **Prevent unbounded memory growth** in long-lived systems: break strong reference chains in destroy/cleanup paths; bound any deduping/caching memory.
- **Preserve semantic invariants**: if a “fast path” changes correctness (e.g., byteLength accuracy used by heuristics), either restore correctness, rename to reflect approximation, or revert.
- **Measure and validate**: benchmark on realistic sizes and avoid tests that overfit nondeterministic GC timing.

**Example pattern (avoid closure allocation when not needed)**
```js
function addDebugInfoIfNeeded(chunk, streamState) {
  if (chunk.status === PENDING || chunk.status === BLOCKED) {
    // Create the closure only in the delayed branch.
    const awaitedInfo = streamState._debugInfo;
    const add = chunk2 => {
      chunk2._debugInfo.push({awaited: awaitedInfo});
    };
    chunk.then(add, add);
  } else {
    // No closure allocation in the common synchronous path.
    chunk._debugInfo.push({awaited: streamState._debugInfo});
  }
}
```

**Rule of thumb:** if a change is framed as “performance”, require (a) reduced allocations/GC or fewer sync/flush operations, and (b) a correctness story (or explicit approximation naming), plus at least lightweight measurement for plausible worst-case inputs.