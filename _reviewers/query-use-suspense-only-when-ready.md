---
title: Use Suspense Only When Ready
description: In Next.js SSR/app-router, do not use `useSuspenseQuery` unless your
  server prefetch + hydration setup guarantees the data is already in the cache such
  that the component will not suspend.
repository: tanstack/query
label: Next
language: Markdown
comments_count: 5
repository_stars: 49380
---

In Next.js SSR/app-router, do not use `useSuspenseQuery` unless your server prefetch + hydration setup guarantees the data is already in the cache such that the component will not suspend.

Why: with standard hydration, if the query isn’t actually present on the client yet, `useSuspenseQuery` may suspend and you’ll get undesirable loading/empty HTML or server/client state mismatch. If you can’t guarantee “no suspend,” prefer `useQuery` (so the component renders with `isLoading`/pending state instead of relying on Suspense streaming).

Apply this rule:
- If you use the “dehydrate pending queries” + streaming-friendly pattern (v5.40+), `useSuspenseQuery` can be appropriate because pending promises can be hydrated and consumed.
- Otherwise (common case with the standard `HydrationBoundary` + awaited prefetch), use `useQuery` in the client component to avoid Suspense-related mismatches.

Also keep SSR hydration details correct:
- For non-JSON serialization, deserialize on the client via `hydrate.transformPromise`.
- Ensure `prefetchQuery({ queryFn })` uses a function `queryFn: () => getPosts().then(serialize)`.

Example (safe default for app-router with awaited prefetch):

```tsx
// app/posts/page.tsx (Server)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query'
import Posts from './posts'
import { getPosts } from './api'

export default async function PostsPage() {
  const queryClient = new QueryClient()
  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Posts />
    </HydrationBoundary>
  )
}

// app/posts/posts.tsx (Client)
'use client'
import { useQuery } from '@tanstack/react-query'
import { getPosts } from './api'

export default function Posts() {
  const { data } = useQuery({ queryKey: ['posts'], queryFn: getPosts })
  return <div>{data?.length}</div>
}
```