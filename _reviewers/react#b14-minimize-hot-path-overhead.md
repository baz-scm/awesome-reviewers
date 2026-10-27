---
title: Minimize Hot-Path Overhead
description: In performance-critical code, avoid adding CPU/memory overhead that blocks
  optimization or causes allocations. Prefer hoisted/module-scope helpers, native
  fast paths, and deferred work when user input is involved—then confirm via benchmarks.
repository: facebook/react#b14
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 251893
---

In performance-critical code, avoid adding CPU/memory overhead that blocks optimization or causes allocations. Prefer hoisted/module-scope helpers, native fast paths, and deferred work when user input is involved—then confirm via benchmarks.

**Do**
- **Avoid closure allocation in hot paths**: only allocate/apply callbacks in the branch that needs them; move shared work to a module-level helper.
- **Prefer native implementations & singletons** for data transforms (e.g., `TextDecoder`), rather than manual chunk loops that allocate/subarray repeatedly.
- **Defer expensive computations** (tree walks, large searches) using `useDeferredValue`/transitions, and surface a pending UI state.
- **Watch for optimizer-deopt patterns**: avoid introducing `try/catch`/extra runtime conditions inside hot functions if you can restructure instead.
- **Reduce memory churn** in large transformations by using index-based continuation instead of repeated `slice`/tail copying.
- **Benchmark/verify impact** for standalone perf-sensitive changes; don’t rely on assumptions.

**Don’t**
- Don’t add extra closures, unnecessary function calls, or branching/try/catch scaffolding in tight loops.
- Don’t rewrite a perf-critical algorithm without measuring whether other serialization/commit paths regressed.

**Example patterns**
1) Hoist helper + allocate closure only when needed:
```js
// module scope
function addDebugInfoEntry(chunk, streamDebugInfo) {
  chunk._debugInfo.push({awaited: streamDebugInfo});
}

function resolveChunkDebugInfo(chunk, streamState) {
  if (chunk.status === PENDING || chunk.status === BLOCKED) {
    const bound = () => addDebugInfoEntry(chunk, streamState._debugInfo);
    chunk.then(bound, bound);
  } else {
    addDebugInfoEntry(chunk, streamState._debugInfo);
  }
}
```
2) Use a native decoder singleton (faster + fewer allocations):
```js
const latin1Decoder = new TextDecoder('latin1');

function binaryToComparableString(view) {
  return latin1Decoder.decode(new Uint8Array(view.buffer, view.byteOffset, view.byteLength));
}
```
3) Defer heavy UI work:
```js
const deferredSearchText = useDeferredValue(searchText);
const searchIsPending = searchText !== deferredSearchText;

// derive matches from deferredSearchText, not searchText
```

Applying these consistently keeps performance predictable by reducing allocation pressure, minimizing deopt risk, and ensuring heavy work doesn’t block interactive updates.