---
title: Correct cache derivations
description: When caching derived computation/type information, ensure the cache is
  both *complete* (stores all relevant dependency sources) and *timed correctly* (updated
  before any code paths read values it depends on).
repository: facebook/react#b12
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 251896
---

When caching derived computation/type information, ensure the cache is both *complete* (stores all relevant dependency sources) and *timed correctly* (updated before any code paths read values it depends on).

Practical rules:
- Don’t restrict cache “sources” to overly narrow cases (e.g., only named identifiers). If derivations can come from other expression shapes, record them so downstream derivation lookups can’t silently miss dependencies.
- When cache state is updated in multi-pass/snapshot loops, preserve the ordering needed for correctness across control flow. If a block’s phi/derived values are used by successor/fallthrough instructions, record those derivations before walking instructions that read them.
- If you’re changing logic to broaden cache recording, add a fixture/test (or at least a TODO) covering the previously-missed cases.

Example (ordering requirement):
```js
// Bad: processing successor instructions before phi derivations are recorded
// would miss x@2 in cache, so type/derivation lookups fail.
if (cond) {
  x = {}; // x@1
}
// x@2 = phi(x@0, x@1)
doSomething(x); // successor reads x@2; phi derivations must already be in cache
```

Example (completeness requirement):
```js
// Good: derivationCache stores source ids for all relevant identifier/expression kinds
// rather than only the named-identifier subset.
context.derivationCache.cache.set(key, {
  sourcesIds: new Set(/* include all derivation-relevant sources */),
});
```