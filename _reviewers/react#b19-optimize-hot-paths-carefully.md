---
title: Optimize hot paths carefully
description: Code that runs on hot paths (per-element, per-chunk, per-node serialization/rendering
  loops) must minimize allocations and call overhead, and any such change must be
  justified with benchmarks rather than assumption.
repository: facebook/react#b19
label: Performance Optimization
language: JavaScript
comments_count: 15
repository_stars: 251893
---

Code that runs on hot paths (per-element, per-chunk, per-node serialization/rendering loops) must minimize allocations and call overhead, and any such change must be justified with benchmarks rather than assumption.

Concretely:
- Avoid unnecessary allocations in loops or frequently-called code: prefer native/optimized APIs (e.g. a module-level `TextDecoder` singleton) over manual chunking; avoid object spreads or array slices/copies per iteration when a plain field/index-based approach works; only allocate closures when actually needed, hoisting reusable logic to module scope and binding lazily (e.g. `fn.bind(reference, arg)` instead of wrapping in `() => fn.call(...)`).
- Avoid extra function-call indirection on hot paths: guard cheap/common cases (e.g. `value[0] === '$'`) before calling into large, non-inlinable functions; add an early return for trivially empty inputs; order checks so the cheap/common case is evaluated before expensive fallback work (e.g. check `delete()` success before scanning an array).
- Don't add branches, extra arguments, or runtime capability checks (e.g. feature detection, try/catch) inside the hottest functions — try/catch and per-call conditionals can block inlining/JIT optimization. Prefer forking a dedicated function/implementation chosen once, over branching every call.
- Keep object property insertion order consistent across code paths that create similar shaped objects, to avoid accidental hidden-class deoptimization; favor inlining small type checks so the VM can share hidden-class checks with surrounding code.
- Never trade correctness or documented contracts for a performance heuristic (e.g. an API that promises an exact value must not silently return an approximation just to save cycles) — if the layering/contract can't tolerate the approximation, drop the optimization.
- Treat any perf-motivated refactor (adding/removing fast paths, changing data structures, splitting functions) as requiring profiling evidence: benchmark before and after, isolate the perf-sensitive change from unrelated refactors, and verify it doesn't regress other call sites that share the modified code.

Example — prefer eager binding over closures, and guard to skip hot-path indirection:
```js
// Avoid: wraps in a fresh closure every call
return encodeFormAction(id, boundPromise, () => defaultEncodeFormAction.call(reference, prefix));

// Prefer: bind once, no closure allocation
return encodeFormAction(id, boundPromise, defaultEncodeFormAction.bind(reference, prefix));

// Avoid: every string pays for entering a large function
return parseModelString(response, parent, key, value);

// Prefer: cheap guard skips the call entirely for the common case
if (value[0] === '$') {
  return parseModelString(response, parent, key, value);
}
return value;
```