---
title: Minimize Allocation Patterns
description: 'In performance-sensitive code, avoid patterns that create unnecessary
  allocations, temporary objects/functions, or hinder engine optimizations.


  Apply these rules:'
repository: facebook/react#b16
label: Performance Optimization
language: JavaScript
comments_count: 11
repository_stars: 251891
---

In performance-sensitive code, avoid patterns that create unnecessary allocations, temporary objects/functions, or hinder engine optimizations.

Apply these rules:
- **Hoist reusable helpers/singletons to module scope** so you don’t recreate them per call/render (e.g. decoders, shared search logic).
- **Allocate closures only when needed**: don’t capture/construct functions outside a conditional when only one branch uses them.
- **Prefer native/fast primitives over allocation-heavy workarounds** (e.g. replace chunked `String.fromCharCode.apply` loops with a single `TextDecoder`).
- **Avoid recursion in hot paths** where listener accumulation could lead to deep call stacks; restructure to check state and call the appropriate “wake/resolve” action directly.
- **Keep object shapes/control flow stable** in hot code to reduce hidden-class churn and deopts (avoid per-call property-layout differences; be cautious with `try/catch` and extra runtime branching in hot paths).
- **Eliminate retention leaks**: when a destroy/unlink hook runs, sever strong reference chains so GC can reclaim old ancestry.

Example (closure allocated only in the delayed branch):
```js
function addDebugInfoEntry(chunk, entry) {
  chunk._debugInfo.push(entry);
}

function maybeAddDebugInfo(chunk, streamState) {
  const entry = {awaited: streamState._debugInfo};
  if (chunk.status === 'pending' || chunk.status === 'blocked') {
    // closure only created for the async path
    const bound = () => addDebugInfoEntry(chunk, entry);
    chunk.then(bound, bound);
  } else {
    addDebugInfoEntry(chunk, entry);
  }
}
```

Example (use a module-level native decoder instead of allocation-heavy loops):
```js
// module scope
const latin1Decoder = new TextDecoder('latin1');

function bytesToComparableString(u8) {
  return latin1Decoder.decode(u8);
}
```

These guidelines help reduce CPU time, GC pressure, and accidental engine slowdowns—especially in hot serialization, client parsing, devtools rendering, and long-lived streaming workloads.