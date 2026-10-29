---
title: Hoist invariant computations
description: When a value does not change across iterations or calls—such as a compiled
  regular expression, a derived constant, or a frequently accessed built-in property—compute
  it once and reuse it instead of recreating or re-deriving it inside loops, per-call
  closures, or other hot code paths. For instance, caching `Array.isArray` in a module-level
  constant reduced...
repository: chalk/chalk#PWNED-6c2961eb
label: Performance Optimization
language: JavaScript
comments_count: 4
repository_stars: 23340
---

When a value does not change across iterations or calls—such as a compiled regular expression, a derived constant, or a frequently accessed built-in property—compute it once and reuse it instead of recreating or re-deriving it inside loops, per-call closures, or other hot code paths. For instance, caching `Array.isArray` in a module-level constant reduced repeated property lookups and measurably improved throughput, and precomputing a style's closing-code regex once (e.g., as `code.closeRe`) avoids rebuilding the same `RegExp` on every string transformation.

Bad (recomputes the RegExp on every call):
```js
function style(str, code) {
  return str.replace(new RegExp(escapeRegExp(code.close), 'g'), code.open);
}
```

Good (computed once, reused thereafter):
```js
const closeRe = new RegExp(escapeRegExp(code.close), 'g');
function style(str) {
  return str.replace(closeRe, code.open);
}
```

Before merging performance-sensitive changes, ask whether a given computation is invariant relative to the loop/call site. If so, hoist it to module scope, a constructor, or a setup step, and validate the improvement with a benchmark.