---
title: Hoist invariant work
description: In hot paths (functions called repeatedly, e.g. styling/formatting code),
  avoid recomputing or re-allocating values that don't change between calls. Precompute
  and cache expensive-to-build objects (like `RegExp` instances) once at module/init
  time instead of rebuilding them on every invocation, cache frequently accessed built-in
  methods or mutable...
repository: chalk/chalk
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 23342
---

In hot paths (functions called repeatedly, e.g. styling/formatting code), avoid recomputing or re-allocating values that don't change between calls. Precompute and cache expensive-to-build objects (like `RegExp` instances) once at module/init time instead of rebuilding them on every invocation, cache frequently accessed built-in methods or mutable properties in module-scope constants to avoid repeated `[[Get]]` lookups, and remove unnecessary wrappers (e.g. IIFEs) that add overhead without benefit. When multiple conditions guard a branch, order them so the cheapest and/or most likely-to-fail check runs first, letting the engine short-circuit before evaluating costlier checks (e.g. check `process.platform` before doing string/array scans). Pull any condition or value that is reused across branches into a single top-level variable instead of recomputing it inline multiple times.

Example:
```js
// Bad: recreates RegExp on every call
function wrap(str, code) {
  return str.replace(new RegExp(escape(code.close), 'g'), code.open);
}

// Good: precompute once
const closeRe = new RegExp(escape(code.close), 'g');
function wrap(str, code) {
  return str.replace(closeRe, code.open);
}
```

When introducing such optimizations, validate the improvement with a benchmark rather than assumption. Prefer benchmarks driven by a minimum runtime (e.g. `set('mintime', 500)`) over manually tuned iteration counts, since arbitrarily low iteration counts can skew or invalidate results.