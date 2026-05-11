---
title: Stable, lifecycle-correct hooks
description: 'Ensure React hooks and query integrations remain correct across renders,
  SSR/hydration, and subscriptions.


  Rules:

  1) Keep QueryClient stable in React components'
repository: tanstack/query
label: React
language: TypeScript
comments_count: 9
repository_stars: 49380
---

Ensure React hooks and query integrations remain correct across renders, SSR/hydration, and subscriptions.

Rules:
1) Keep QueryClient stable in React components
- Create it once using one of: `React.useState(() => new QueryClient())`, `React.useMemo(() => new QueryClient(), [])`, or a lazy `useRef` initializer.
- Avoid `new QueryClient()` directly in component render.
- In Server Components, creating a new `QueryClient` per request is fine.

2) Don’t break subscription/snapshot invariants
- Avoid reading refs (or mutating derived values) during render for SyncExternalStore/getSnapshot-style logic.
- If you need “latest filters/options”, update a ref in `useEffect`, and read the real source of truth inside the correct React lifecycle (e.g., `getSnapshot`) rather than during render.

3) Hydration-safe first render
- Make the initial/optimistic state that React renders match the server render.
- If stale data requires a refetch, trigger it after the first render/mount to prevent hydration mismatches.

4) Use supported disabling patterns
- If you want to disable conditionally, prefer `skipToken` over returning/defining a queryFn that will error while `enabled: false` patterns would otherwise spam logs.

Example (stable QueryClient + latest filters ref pattern):
```tsx
import React from 'react'
import { QueryClient } from '@tanstack/react-query'

export function App() {
  const [queryClient] = React.useState(() => new QueryClient())

  // ...useQuery hooks using queryClient
  return null
}
```

And for “latest value” without render-time ref reads:
```tsx
const [state, setState] = React.useState(() => client.isFetching(initialFilters))
const filtersRef = React.useRef(filters)
React.useEffect(() => {
  filtersRef.current = filters
}, [filters])
// Ensure the snapshot/getter reads in the right lifecycle, not during render-time ref reads.
```