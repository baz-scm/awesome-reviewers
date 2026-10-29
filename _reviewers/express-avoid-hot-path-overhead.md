---
title: Avoid hot-path overhead
description: In performance-sensitive, frequently-executed code paths (per-request
  handlers, middleware, core request/response methods), minimize unnecessary allocations,
  indirection, and repeated expensive operations, and justify optimizations with real
  benchmarks rather than assumptions.
repository: expressjs/Express
label: Performance Optimization
language: JavaScript
comments_count: 8
repository_stars: 69579
---

In performance-sensitive, frequently-executed code paths (per-request handlers, middleware, core request/response methods), minimize unnecessary allocations, indirection, and repeated expensive operations, and justify optimizations with real benchmarks rather than assumptions.

Guidelines:
- Prefer simple, direct operations over heavier constructs when both are correct. For example, use a plain character check/slice instead of a regex for trivial string trimming:
  ```js
  // Preferred over hostname.replace(/\.$/, '')
  if (hostname[hostname.length - 1] === '.') {
    hostname = hostname.slice(0, -1);
  }
  ```
- Use plain `for` loops instead of `Array.prototype.forEach`/closures in hot internal code paths to avoid closure-creation overhead.
- Never perform expensive one-time setup (e.g. `require()` of optional/conditional modules) inside a per-request or per-call code path; do it once at module load time so failures/successes are cached appropriately.
- Don't add streaming/wrapping abstractions (e.g. wrapping an already-fully-buffered value in a Readable stream) when the data is already fully in memory—this adds overhead without real backpressure benefits. Only stream when the underlying source can genuinely be read incrementally (disk, network, generator).
- When introducing internal fast paths (e.g., direct property assignment instead of calling a public setter), confirm there is no required validation being bypassed, and prefer the fast path internally when validation is unnecessary.
- Any performance trade-off (e.g., try/catch for fast-path decoding vs. fallback behavior) should be backed by actual benchmark numbers comparing both paths under realistic inputs, and these numbers should be documented in the PR/commit.
- When adding or modifying benchmarks, ensure they exercise the actual code paths/options relevant to the change (e.g., compare the library's own configurable options against each other) rather than only measuring an underlying third-party dependency.

Following these practices keeps hot paths lean, avoids regressions from "nice to have" abstractions, and ensures performance claims are measurable and reproducible.