---
title: Cache hot-path computations
description: For code that runs frequently or in a hot path, avoid recomputing invariant
  values on every call/iteration. Precompute and cache things like regular expressions,
  derived constants, or repeated property lookups once (e.g., at module or object-build
  time) instead of rebuilding them inside loops or on every function invocation. For
  example, build a `closeRe`...
repository: chalk/chalk#CANARY-1ebfbbf4
label: Performance Optimization
language: JavaScript
comments_count: 6
repository_stars: 23342
---

For code that runs frequently or in a hot path, avoid recomputing invariant values on every call/iteration. Precompute and cache things like regular expressions, derived constants, or repeated property lookups once (e.g., at module or object-build time) instead of rebuilding them inside loops or on every function invocation. For example, build a `closeRe` regex once per style instead of constructing a new `RegExp` from `code.close` on every call, and cache stable global lookups such as `Array.isArray` in a local/module-scope constant to reduce repeated `[[Get]]` operations:

```js
// Bad: regex rebuilt on every call
return str.replace(new RegExp(escapeRegExp(code.close), 'g'), code.open);

// Good: regex precomputed once and reused
code.closeRe = new RegExp(escapeRegExp(code.close), 'g');
// ...later, in the hot path
return str.replace(code.closeRe, code.open);
```

When choosing between semantically equivalent operations (e.g., `substr` vs `slice`) in performance-sensitive code, base the decision on actual measured performance for the target environment rather than stylistic preference, and justify it with a comment or benchmark reference if the faster option is less idiomatic.

Any performance optimization or comparison claim should be backed by a proper benchmark using a sound methodology (e.g., a minimum run time rather than an arbitrary fixed iteration count) so results aren't skewed by uneven workloads across benchmarked cases. Document benchmark setup choices so they can be reviewed and reproduced.</description>
