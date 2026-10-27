---
title: Hot-path allocation discipline
description: 'In code that runs on hot paths (serialization, parsing, rendering, event
  dispatch), minimize work and memory churn, and avoid patterns that prevent JIT optimizations:'
repository: facebook/react#b18
label: Performance Optimization
language: JavaScript
comments_count: 16
repository_stars: 251889
---

In code that runs on hot paths (serialization, parsing, rendering, event dispatch), minimize work and memory churn, and avoid patterns that prevent JIT optimizations:

- Avoid allocating closures, objects, or arrays inside loops or on every call. Prefer `Function.prototype.bind` or a module-scope function reused across call sites instead of creating a new inline closure each time; if a closure is only needed on one branch, allocate it only in that branch, e.g.:
```js
if (chunk.status === PENDING || chunk.status === BLOCKED) {
  const boundAddDebugInfo = addDebugInfo.bind(null, chunk);
  chunk.then(boundAddDebugInfo, boundAddDebugInfo);
} else {
  addDebugInfo(chunk);
}
```
- Keep object shapes (hidden classes) stable: construct objects with all properties present and in a consistent order instead of adding properties conditionally later, and make optional fields required where possible.
- Avoid unbounded recursion in paths that can be invoked many times (e.g. listener fan-out); instead check state and dispatch with a flat check-then-call pattern to avoid stack-overflow risk.
- Put the cheapest/most common check first so expensive work (loops, allocations) is skipped in the common case, e.g. check `size === 0` or whether a delete already succeeded before running a scan loop.
- Avoid deopt-prone constructs (e.g. `try/catch`, `arguments`, polymorphic shapes) in code that must be as fast as possible; prefer letting unsupported operations throw rather than guarding every call with try/catch.
- Prefer simple `typeof`/shape checks over heavier APIs (e.g. `typeof x === 'string'` vs `Array.isArray`) when they are cheaper and equivalent, and keep such checks inlined near their use rather than factored into tiny helper functions, since inlining lets the VM share hidden-class checks across adjacent code.
- When a hot function needs different behavior for a rare case, fork a specialized version instead of adding extra parameters/branches to the hot function.
- Avoid repeating expensive work across continuations/iterations (e.g. re-slicing or copying the remaining portion of a large array for every chunk); prefer tracking an index/offset instead of copying remaining data.
- Never sacrifice correctness for an unverified or marginal performance gain: any approximation (e.g. treating byte length as string length) must be clearly named and audited everywhere it's consumed, and should be dropped unless it yields a measurable, significant win.
- Validate performance claims before committing a technique: benchmark actual before/after results for the specific hot path affected, and double-check that optimizations for one case (e.g. captured stack traces) don't leave other retained objects/leaks unaddressed.

Apply these checks specifically to code identified as hot (renderer fibers, Flight server/client serialization, DOM event dispatch, performance tracking); outside hot paths, prefer the version that's easier to read unless profiling shows it matters.