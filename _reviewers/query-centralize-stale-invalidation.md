---
title: Centralize Stale Invalidation
description: When implementing or modifying caching/fetch decisions, treat “fresh
  vs stale” as a single source of truth derived from the query’s invalidation + stale-time
  logic. Avoid adding ad-hoc fetch conditions at the observer/queryClient level that
  bypass (or redefine) TTL semantics.
repository: tanstack/query
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 49380
---

When implementing or modifying caching/fetch decisions, treat “fresh vs stale” as a single source of truth derived from the query’s invalidation + stale-time logic. Avoid adding ad-hoc fetch conditions at the observer/queryClient level that bypass (or redefine) TTL semantics.

Concrete rules:
1) Model semantic events (e.g., “background error while data exists”) by updating invalidation state in the query/state layer (e.g., set `isInvalidated: true`).
   - Fetch decision code should rely on `isStale()` / existing stale-time helpers, not on `status === 'error'` special-cases.
2) Preserve `staleTime` meaning.
   - `ensureQueryData`/`prefetchQuery` should decide whether to return cached data now vs kick off a background fetch; they should not silently reinterpret the option (e.g., don’t turn “prefetch threshold” into “global query staleTime”).
3) If you implement TTL via timers:
   - Recompute `isInvalidated` when `staleTime` changes.
   - When `staleTime === 0`, mark as invalidated deterministically.
   - After state/data updates (e.g., reducer runs), recompute and update/clear the stale timer accordingly.
4) Keep fetch orchestration scope-safe.
   - If hydration/pending logic affects whether background fetches run, scope it per `QueryClient` and ensure SSR-derived state is sanitized so client hydration reuses the intended freshness state.

Example pattern (central invalidation drives fetch):
```ts
// In reducer/state update (when an error happens during a background refetch
// and existing data remains):
return {
  ...state,
  status: 'error',
  isInvalidated: true, // centralize semantic freshness change here
}

// In fetch decision logic (observer/queryObserver):
const shouldFetch = value === 'always' || (value !== false && query.isStale())
```

Applying these rules prevents subtle regressions like `staleTime: 'static'` data being refetched due to observer-level error checks, and avoids TTL drift when `staleTime` or data updates occur.