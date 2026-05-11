---
title: Resolve predicates, seed reducers
description: 'When building or extending algorithmic pipelines (streaming, reduction,
  conditional processing), ensure two correctness points:


  1) Resolve dynamic conditions before acting'
repository: tanstack/query
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 49380
---

When building or extending algorithmic pipelines (streaming, reduction, conditional processing), ensure two correctness points:

1) Resolve dynamic conditions before acting
- If an option (e.g., “enabled”) can be a callback/function, resolve it to a concrete boolean using the library’s resolver (e.g., `resolveEnabled`) rather than treating it as a static flag.

2) Define the reducer’s initial accumulator/seed
- Ensure the first reducer invocation receives a predictable accumulator.
- Prefer matching native `reduce` semantics: either require/provide an explicit initial value, or implement the same “no initial value uses the first element as the seed” behavior.

Example (pattern):
```ts
// 1) Resolve a dynamic predicate before selecting work
const shouldProcess = (query: any) =>
  query.state.status === 'error' &&
  query.getObserversCount() > 0 &&
  query.observers.some((observer: any) =>
    resolveEnabled(observer.options.enabled, query), // resolve callback-based enabled
  )

// 2) Seed a reducer deterministically
function reduceChunks<TChunk, TAcc>(chunks: TChunk[], reducer: (acc: TAcc, c: TChunk) => TAcc, initial: TAcc) {
  let acc = initial
  for (const chunk of chunks) acc = reducer(acc, chunk)
  return acc
}
```
Apply this standard to prevent “first-step” surprises (wrong/empty accumulator) and to avoid silently skipping or incorrectly processing work due to unresolved callback-based conditions.