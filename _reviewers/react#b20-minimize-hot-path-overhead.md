---
title: Minimize hot-path overhead
description: 'In code that runs on hot paths (serialization, rendering, event dispatch,
  string/object processing), every extra allocation, branch, or indirection adds up
  and should be deliberately avoided and verified with benchmarks:'
repository: facebook/react#b20
label: Performance Optimization
language: JavaScript
comments_count: 12
repository_stars: 251895
---

In code that runs on hot paths (serialization, rendering, event dispatch, string/object processing), every extra allocation, branch, or indirection adds up and should be deliberately avoided and verified with benchmarks:

- Avoid unnecessary allocations: prefer `fn.bind(obj, arg)` over wrapping in an arrow-function closure when forwarding a reference; avoid spreading/copying objects (`{...data, ...}`) just to iterate or pass data around, especially inside loops that run per-node or per-render.
- Keep object shapes stable for the VM's hidden-class optimizations: always set properties in the same order, and declare properties (even if initially empty, e.g. `nonce?: ?Chunk`) as required/always-present rather than adding them conditionally later, so hidden classes aren't needlessly duplicated.
- Avoid redundant work and repeated copies: when continuing/splitting large data structures (e.g., slicing array tails for continuation tasks), prefer index-based iteration over copying/slicing the remaining data on every step.
- Guard expensive calls with cheap early checks when it avoids entering large, non-inlinable functions (e.g., check `value[0] === '$'` before calling into a large switch-based parser), but don't duplicate checks purely out of habit — only add the guard when it measurably avoids function-call overhead.
- Prefer forking/specializing a function for a new hot-path use case over adding new parameters/branches to an already-hot shared function (e.g., fork `emitChunk`/`tryStreamTask` rather than adding an `isByteStream` flag).
- Keep small, frequently-called type/shape-check helpers inlined at their call sites rather than extracting them into separate functions, so the VM can share hidden-class checks with surrounding code.
- Don't sacrifice correctness for a perf shortcut unless the approximation is clearly documented/renamed (e.g., don't silently return an approximate byte length from a function named `byteLengthOfChunk`), and make sure all call sites that rely on exact values are audited first.
- Bound memory growth from caches/dedup tables under load with a fixed total size budget rather than independent per-entry limits that can multiply and blow past the intended memory ceiling.
- Any change motivated primarily by performance (especially ones affecting shared/hot code paths) must be validated with before/after benchmarks; if official benchmarks don't cover the path (e.g., RSC/Flight), add one or share repeatable numbers in the PR before landing the change.

Example — avoiding a closure allocation:
```js
// Avoid: allocates a new closure on every call
return encodeFormAction(referenceClosure.id, boundPromise, () =>
  defaultEncodeFormAction.call(reference, identifierPrefix),
);

// Prefer: bind reuses existing semantics without an extra closure
return encodeFormAction(
  referenceClosure.id,
  boundPromise,
  defaultEncodeFormAction.bind(reference, identifierPrefix),
);
```