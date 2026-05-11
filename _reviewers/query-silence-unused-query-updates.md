---
title: Silence Unused Query Updates
description: 'To optimize performance, prevent components from re-rendering when they
  don’t need to react to query updates.


  **Rule:** If you use `useQuery`/`useFocusEffect` for *prefetching* or *side effects*
  and intentionally *ignore the result*, disable change notifications so the hook
  doesn’t subscribe to updates that would trigger re-renders.'
repository: tanstack/query
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 49380
---

To optimize performance, prevent components from re-rendering when they don’t need to react to query updates.

**Rule:** If you use `useQuery`/`useFocusEffect` for *prefetching* or *side effects* and intentionally *ignore the result*, disable change notifications so the hook doesn’t subscribe to updates that would trigger re-renders.

### Apply to React Query prefetching (ignore result)
When you “prefetch by calling `useQuery` but not using `data`”, you still create an observer and can cause re-renders. Pass an empty `notifyOnChangeProps` to avoid notifications.

```tsx
function Article({ id }: { id: string }) {
  // Critical data used by UI
  const { data: articleData, isPending } = useQuery({
    queryKey: ['article', id],
    queryFn: getArticleById,
  })

  // Prefetch-only: prevent re-renders
  useQuery({
    queryKey: ['article-comments', id],
    queryFn: getArticleCommentsById,
    notifyOnChangeProps: [],
  })

  if (isPending) return 'Loading article...'
  return <Comments id={id} articleData={articleData} />
}
```

### Apply to React Navigation focus
If screen UI should not update while out of focus, gate notifications so query-driven state won’t re-render off-screen.

In practice, implement a focus-aware `notifyOnChangeProps` (optionally using `navigation.isFocused()` if available) so that updates are suppressed while unfocused and re-enabled when focused again.
