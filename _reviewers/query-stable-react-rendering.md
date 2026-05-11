---
title: Stable React Rendering
description: Write React components and tests so they don’t depend on React’s internal
  render/callback sequencing, and so Suspense boundaries capture the work that actually
  suspends.
repository: tanstack/query
label: React
language: TSX
comments_count: 7
repository_stars: 49380
---

Write React components and tests so they don’t depend on React’s internal render/callback sequencing, and so Suspense boundaries capture the work that actually suspends.

Apply:
- Put the suspending query/resource inside the component that’s rendered *within* the Suspense boundary (move query hooks into a child component).
- Don’t use boolean “first/last render” assumptions or logic tied to how many times React calls callbacks; React 19 can change counts/order.
- Base tests on observable state/DOM output; if React 18 vs 19 truly differs, branch expectations by version.
- Prefer effects for client-only orchestration/updates; use lazy initializers for `useState` when constructing objects.

Example (Suspense + boundary correctness):
```tsx
import { createQuery } from '@tanstack/solid-query' // or equivalent React Query patterns
import React, { Suspense } from 'react'

function Posts({ postId }: { postId: number }) {
  const query = createQuery(() => ({
    queryKey: ['posts', postId],
    queryFn: () => fetch('/api/posts/' + postId).then(r => r.json()),
  }))

  return <div>{String(query.data?.title ?? '')}</div>
}

export function Home() {
  const [postId, setPostId] = React.useState(1)

  return (
    <>
      <button onClick={() => setPostId(id => Math.max(1, id - 1))}>Prev</button>
      <button onClick={() => setPostId(id => id + 1)}>Next</button>

      <Suspense fallback={<div>Loading post...</div>}>
        <Posts postId={postId} />
      </Suspense>
    </>
  )
}
```

Example (avoid render-count assumptions):
```ts
// Instead of: if (!boundary) { ... }
// Use count/state-based expectations or version-conditional assertions.
let callCount = 0
const useErrorBoundary = () => (++callCount, callCount < 3)
```