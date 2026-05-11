---
title: Control focus and suspense
description: 'When implementing React hooks around navigation focus or React Suspense:


  1) Treat focus/mount as distinct

  - If you use `useFocusEffect` to run data refetches, remember the callback also
  runs on initial mount. Skip the first run when appropriate.'
repository: tanstack/query
label: React
language: Markdown
comments_count: 6
repository_stars: 49380
---

When implementing React hooks around navigation focus or React Suspense:

1) Treat focus/mount as distinct
- If you use `useFocusEffect` to run data refetches, remember the callback also runs on initial mount. Skip the first run when appropriate.
- Effects clean up when the screen/component goes out of focus.

2) For Suspense + prefetch, don’t “prefetch with suspense”
- If the goal is to warm the cache without extending the current Suspense fallback, use dedicated prefetch hooks (e.g., `usePrefetchQuery` / `usePrefetchInfiniteQuery`) rather than forcing suspense queries just to prefetch.

3) Avoid re-renders for non-UI-affecting query observers
- When you mount a query only to trigger background fetching (and not to render its result), suppress observer-triggered updates (e.g., `notifyOnChangeProps: []`).

4) Don’t expect `placeholderData` to work with `useSuspenseQuery`
- With suspense, loading UI is handled by Suspense/ErrorBoundary; use `startTransition` when changing query keys to avoid unwanted fallback churn.

Example (focus refetch with correct skip, plus cache-warming prefetch without suspense):

```tsx
import { useFocusEffect } from '@react-navigation/native'
import { useQueryClient } from '@tanstack/react-query'

function useRefreshOnFocus(refetch: () => Promise<unknown>) {
  const queryClient = useQueryClient()

  useFocusEffect(
    // If you keep local “first run” logic, ensure you skip the initial mount run.
    (callback) => {
      // callback pattern used by React Navigation; you can also use a ref.
      let isFirst = true

      const run = async () => {
        if (isFirst) {
          isFirst = false
          return
        }
        // Prefer explicit query behavior rather than always invoking refetch()
        queryClient.refetchQueries({ queryKey: ['posts'], stale: true, type: 'active' })
      }

      run()
      return callback()
    },
    [queryClient]
  )
}
```

Key checklist before approving PRs:
- Does `useFocusEffect` logic explicitly handle the initial mount run?
- Do you use prefetch-only hooks for Suspense prefetching (not suspense queries)?
- Are “background-only” queries preventing unnecessary re-renders (`notifyOnChangeProps: []`)?
- Are you using `startTransition` for query-key updates instead of relying on `placeholderData` with `useSuspenseQuery`?