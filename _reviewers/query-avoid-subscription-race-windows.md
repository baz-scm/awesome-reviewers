---
title: Avoid subscription race windows
description: When code derives state from an external cache/store (or wraps promises),
  treat subscription setup and promise resolution as concurrent events. Ensure your
  implementation is race-safe and doesn’t use stale inputs.
repository: tanstack/query
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 49380
---

When code derives state from an external cache/store (or wraps promises), treat subscription setup and promise resolution as concurrent events. Ensure your implementation is race-safe and doesn’t use stale inputs.

Apply these rules:
1) Close the “init-before-subscribe” race: after creating/obtaining the source (store/cache) and before/while wiring the subscription callback, immediately sync derived state so updates that occur in the setup window aren’t missed.
2) Resubscribe when dependencies change: if filters/select/query keys change, recreate the subscription (don’t keep listening with old options).
3) Don’t let non-critical async failures abort whole batches: avoid throwing inside Promise.all-mapped work for cases you can ignore; handle per-item errors and continue.
4) For promise/thenable proxies and concurrent fetch/cancel/resolve, define expected behavior and add tests for ordering edge-cases.

Example pattern (React-like):
```ts
useEffect(() => {
  // 1) Sync immediately to avoid missing updates in the setup window
  setResult(getResult(store, optionsRef.current))

  // 2) Subscribe for subsequent updates
  const unsubscribe = store.subscribe(() => {
    setResult(getResult(store, optionsRef.current))
  })

  return unsubscribe
}, [store /* and ensure resubscribe when options/select changes if needed */])
```

Example pattern (Solid-like):
```ts
createEffect(() => {
  const unsub = mutationCache().subscribe(() => {
    setResult(getResult(mutationCache(), options()))
  })
  onCleanup(unsub)
})
```

Example for Promise.all: don’t throw for “not-a-thing we care about”.
```ts
await Promise.all(
  Object.keys(deps ?? {}).map(async dep => {
    const depPackage = packages.find(p => p.name === dep)
    if (!depPackage) return // ignore non-critical/non-matching deps
    // ...do work for relevant deps
  })
)
```