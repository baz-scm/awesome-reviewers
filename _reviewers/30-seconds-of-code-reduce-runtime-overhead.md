---
title: Reduce runtime overhead
description: 'When optimizing performance, remove repeated work in hot paths: avoid
  per-call overhead, extra passes over the same data, and unnecessary allocations;
  validate choices with benchmarks.'
repository: 30-seconds/30-seconds-of-code
label: Performance Optimization
language: Markdown
comments_count: 4
repository_stars: 129334
---

When optimizing performance, remove repeated work in hot paths: avoid per-call overhead, extra passes over the same data, and unnecessary allocations; validate choices with benchmarks.

Apply these rules:
- Keep imports/`require` at module scope (not inside functions).
- Prefer single-pass logic over multi-pass pipelines (`map`+`filter`+`reduce`), especially when you can early-return or accumulate in one traversal.
- Avoid creating new objects/closures/large strings on every call in high-traffic code.
- When tradeoffs aren’t obvious, benchmark.

Examples:
```js
// 1) Import once (module scope)
const crypto = require('crypto');
const hashNode = value => crypto.createHash('sha256').update(String(value)).digest('hex');

// 2) Avoid extra passes (single traversal + early result)
const dig = (obj, target) =>
  target in obj
    ? obj[target]
    : Object.values(obj).reduce((acc, v) => (acc !== undefined ? acc : typeof v === 'object' ? dig(v, target) : undefined), undefined);

// 3) Don’t allocate per log in hot code paths
// Prefer separate functions/constants per option instead of rebuilding large strings/objects every call.
```