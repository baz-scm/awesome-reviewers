---
title: Stable Index Mapping
description: 'Prefer stable data-structure lookups over recomputing indices in update
  paths—especially when the underlying collection can reorder.


  **Guideline**

  1. **Avoid linear searches in hot paths**: if you need an element’s position during
  frequent updates, don’t use patterns like `array.indexOf(x)` repeatedly. Use a map
  (e.g., `WeakMap`/`Map`) that gives the...'
repository: tanstack/query
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 49380
---

Prefer stable data-structure lookups over recomputing indices in update paths—especially when the underlying collection can reorder.

**Guideline**
1. **Avoid linear searches in hot paths**: if you need an element’s position during frequent updates, don’t use patterns like `array.indexOf(x)` repeatedly. Use a map (e.g., `WeakMap`/`Map`) that gives the current index in O(1).
2. **Preserve invariants under reordering**: if you consider capturing an `index` in a subscription/callback, ensure that index remains valid after operations like `setQueries()` reorder the internal list. If not, don’t capture the position—compute it via the maintained map at update time.
3. **Add regression tests for subtle ordering/shape issues**:
   - Ordering: tests should cover reordering while subscriptions are active, and verify result placement after updates/invalidation.
   - Aggregation semantics: when appending streamed chunks, ensure you don’t accidentally change array dimensionality (e.g., avoid implicit flattening).

**Example (index stability + O(1) lookup)**
```ts
// Bad: recomputes position each update (and may be O(n))
function onUpdate(observer: Observer, result: Result) {
  const index = observers.indexOf(observer) // linear + fragile
  if (index !== -1) results[index] = result
}

// Good: keep a maintained index map and look up at update time
const indexMap = new WeakMap<Observer, number>()

function onUpdate(observer: Observer, result: Result) {
  const index = indexMap.get(observer)
  if (index !== undefined) results[index] = result
}
```

**Example (stream aggregation shape correctness)**
```ts
// If TQueryFnData could itself be an array, avoid implicit flattening:
// concat(chunk) may flatten a chunk when chunk is an array.
result = prev.concat([chunk]) // keeps 1-dimensional “array of chunks” shape
```