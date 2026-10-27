---
title: Hot-Path Allocation Rules
description: 'When code runs frequently (render/serialization, tracing, streaming,
  diff/attach loops), treat performance as a first-class correctness constraint: eliminate
  avoidable allocations and de-optimizing constructs, and prefer native/engine-optimized
  primitives.'
repository: facebook/react#b9
label: Performance Optimization
language: JavaScript
comments_count: 8
repository_stars: 251891
---

When code runs frequently (render/serialization, tracing, streaming, diff/attach loops), treat performance as a first-class correctness constraint: eliminate avoidable allocations and de-optimizing constructs, and prefer native/engine-optimized primitives.

Apply these guidelines:
- **Hoist and reuse:** move helper functions, decoders, and constants to module scope; avoid per-call `bind`, per-branch closure allocation, and repeated object copies/spreads in loops.
- **Prefer native APIs:** replace manual byte→string loops/chunking with built-in decoders when they meet invariants; keep mappings bijective when required.
- **Avoid engine deopts in hot functions:** don’t place `try/finally` (or similar deopt triggers) in the hottest enclosing scope—wrap the minimal code in a tiny helper instead.
- **Reduce allocation churn in algorithms:** avoid repeated `slice`/tail copying in long-array continuation patterns; use index-based approaches when possible.
- **Control GC retention:** in long-lived async/debug/streaming workloads, sever strong reference chains during destroy/cleanup to prevent unbounded memory growth.
- **Be explicit about scheduling:** for UI-derived expensive computations, compute from deferred values and show a pending indicator rather than blocking input.

Example pattern (hoist + avoid closure allocation):
```js
// Bad in hot path: per-call closure/`bind`
function hot(ref, id, identifierPrefix) {
  return encodeFormAction(
    id,
    Promise.resolve([]),
    () => defaultEncodeFormAction.call(ref, identifierPrefix),
  );
}

// Better: reuse a module-level helper so the closure allocates only when needed
function encodeFallback(ref, identifierPrefix) {
  return defaultEncodeFormAction.call(ref, identifierPrefix);
}

function hot(ref, id, identifierPrefix) {
  const bound = () => encodeFallback(ref, identifierPrefix);
  return encodeFormAction(id, Promise.resolve([]), bound);
}
```
Use the same principle more broadly: move stable computation out of loops/call sites, and restructure to avoid per-iteration allocations and deopts.