---
title: Scoped cache reset rules
description: 'When code triggers cache reset/refetch or relies on cached freshness,
  make the behavior intentionally scoped and snapshot-correct:


  - Scope reset-triggered refetches to the intended cache region:'
repository: tanstack/query
label: Caching
language: TSX
comments_count: 5
repository_stars: 49380
---

When code triggers cache reset/refetch or relies on cached freshness, make the behavior intentionally scoped and snapshot-correct:

- Scope reset-triggered refetches to the intended cache region:
  - Prefer predicates that limit refetch to relevant queries (e.g., only queries in error state, with active observers, and that are still effectively enabled).
  - Do not “global refetch” without guardrails, since cache resets can otherwise restart disabled work or cause unexpected churn.

- Don’t assert refetch-by-default semantics that conflict with freshness/floor rules:
  - If a mode enforces a minimum staleTime (e.g., Suspense), tests and calling code must expect the “freshness floor” behavior rather than immediate refetch on remount.

- Use stable, unique query keys in caching tests and reproduction:
  - Use the provided helpers/utilities for unique keys to avoid cross-test cache pollution.

- Snapshot per-operation metadata in cached records:
  - Ensure mutation/query records store the correct meta for each operation, even when meta changes after a re-render between mutations.

Example pattern for scoped reset refetch (adapted):
```ts
function createValue(client?: QueryClient) {
  let isReset = false
  return {
    clearReset: () => { isReset = false },
    reset: () => {
      isReset = true
      void client?.refetchQueries({
        predicate: (query) =>
          query.state.status === 'error' &&
          query.getObserversCount() > 0 &&
          query.observers.some(
            (observer) => resolveEnabled(observer.options.enabled, query) !== false,
          ),
      })
    },
  }
}
```

Practical checklist:
- If you add/modify reset/refetch logic: add/verify predicates for relevance + enabled/intent.
- If you modify caching freshness behavior: update tests to match the current staleTime/freshness contract.
- If you add caching-related tests: always use unique query keys (via helpers).
- If you change mutation meta handling: add a test that meta updated between mutations results in distinct cached meta snapshots for each mutation.