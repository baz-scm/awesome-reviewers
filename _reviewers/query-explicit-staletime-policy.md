---
title: Explicit StaleTime Policy
description: 'For every query, define a clear staleness/refetch policy—especially
  for SSR/hydration—rather than relying on defaults or assumptions.


  **Standards**

  - **Always choose `staleTime` deliberately** (default is `0`, which means cached
  data is treated as stale).'
repository: tanstack/query
label: Caching
language: Markdown
comments_count: 6
repository_stars: 49380
---

For every query, define a clear staleness/refetch policy—especially for SSR/hydration—rather than relying on defaults or assumptions.

**Standards**
- **Always choose `staleTime` deliberately** (default is `0`, which means cached data is treated as stale).
- **Understand `staleTime: Infinity` vs `staleTime: 'static'`:** 
  - With `Infinity`, “always” refetch triggers can still fire.
  - With `'static'`, those “always” triggers won’t revive the query; you must explicitly reset/clear via the query client.
- **Hydration:** `HydrationBoundary` prevents unnecessary refetching during hydration; hydrated queries will only refetch on mount if `refetchOnMount: 'always'` is explicitly set.
  - Ensure the UX/markup matches SSR first (render stale data), then refetch if it’s stale.
- **Prefetching:** don’t assume `prefetchQuery` uses the same freshness config as your `useQuery` observers. If you didn’t provide a `staleTime`/defaults, the call may treat cached data as stale (default `0`).
- **Error recovery:** cached “not stale” data must not block refetch/retry when the query is in an error state—configure so error state still triggers recovery.
- **SSR cache lifetime:** avoid `gcTime: 0` as it can cause hydration errors; be intentional about cache retention.

**Example (SSR + explicit stale/refetch intent)**
```ts
// query defaults (e.g., in your QueryClient)
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // pick one intentionally
      staleTime: 'static', // or Infinity, or a number
      // for hydration: only force mount refetch when truly needed
      refetchOnMount: 'always',
      // error recovery should still happen (ensure your retry policy allows it)
      retry: 2,
    },
  },
})

// SSR/CSR: render via HydrationBoundary to prevent unnecessary hydration refetch
return (
  <HydrationBoundary state={dehydratedState}>
    <App />
  </HydrationBoundary>
)
```

**Practical checklist for PRs**
- What is the intended `staleTime` (number / `Infinity` / `'static'`)?
- Should hydration refetch on mount (`refetchOnMount`), and why?
- If using prefetching, did you ensure the staleness policy matches expectations?
- If the query can error, what ensures refetch/retry still recovers users?