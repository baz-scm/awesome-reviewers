---
title: Cache Derived Sets
description: When analyzing or transforming IR/AST, avoid re-creating expensive derived
  data structures inside loops (e.g., allocating a new `Set` for every `filter`/`map`
  iteration). Build the derived structure once per pass, reuse it, and keep “lazy
  until error” patterns only if they meaningfully reduce work and don’t obscure intent.
  If you add extra whole-function...
repository: facebook/react#b4
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251885
---

When analyzing or transforming IR/AST, avoid re-creating expensive derived data structures inside loops (e.g., allocating a new `Set` for every `filter`/`map` iteration). Build the derived structure once per pass, reuse it, and keep “lazy until error” patterns only if they meaningfully reduce work and don’t obscure intent. If you add extra whole-function traversals, add a brief cost note and/or measurement.

Example (fix repeated `Set` allocation):

```ts
// Bad: creates a new Set on every filter callback
const rvalues = rvaluesUnfiltered.filter(place =>
  !state.inScope(startId, place) || state.identifiers.has(place.identifier.id)
);
...
undefinedIdentifiers = () =>
  (undefinedIdentifiers?.() ?? []).concat(
    rvaluesUnfiltered.filter(v => new Set(rvalues).has(v))
  );

// Better: cache Set once
const rvaluesSet = new Set(rvalues);
undefinedIdentifiers = () =>
  (undefinedIdentifiers?.() ?? []).concat(
    rvaluesUnfiltered.filter(v => rvaluesSet.has(v))
  );
```

If you do defer expensive work until errors, prefer a simple `let result: Set/Array | null` or similar unless there’s a clear, measured reason to keep it as a function; otherwise optimize for clarity first.