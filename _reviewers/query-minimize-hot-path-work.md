---
title: Minimize Hot-Path Work
description: When working on performance-sensitive code (query observers, hydration,
  render-triggering state, hot utilities), ensure you only do the necessary work and
  no redundant allocations/wrappers, while also preventing leaks.
repository: tanstack/query
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 49380
---

When working on performance-sensitive code (query observers, hydration, render-triggering state, hot utilities), ensure you only do the necessary work and no redundant allocations/wrappers, while also preventing leaks.

Apply these rules:
- Avoid unnecessary network/UI work: don’t enable fetch/retry paths when data is already synchronously available—add/keep tests that assert loading-state transitions.
- Make change detection “minimal but correct”: compare the specific fields that can affect rendering; missing metadata/derived fields can silently block required recomputation, while incorrect comparisons can trigger extra recomputations.
- Eliminate repeated allocations in loops/hot paths: precompute data structures used by callbacks (e.g., create a `Set` once, not per `filter` iteration).
- Avoid redundant expensive computations: don’t call deep-compare/structural-sharing helpers twice when you can short-circuit.
- Wrap expensive logic once, not per-page/per-iteration.
- Always clean up long-lived resources (subscriptions, BroadcastChannels, event listeners) to prevent gradual performance degradation.

Example (single Set allocation in a hot utility):
```ts
function difference<T>(array1: T[], array2: T[]): T[] {
  const set2 = new Set(array2)
  return array1.filter((x) => !set2.has(x))
}
```

Example (wrap fetch once when a persister exists):
```ts
if (context.options.persister) {
  context.fetchFn = () =>
    context.options.persister!(fetchFn as any, {
      queryKey: context.queryKey,
      meta: context.options.meta,
      signal: context.signal,
    })
}
```