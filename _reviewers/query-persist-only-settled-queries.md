---
title: Persist Only Settled Queries
description: When using async/concurrent flows (streaming, dehydration/rehydration,
  optimistic updates), ensure you never persist “in-flight” async state and you always
  return promises from async callbacks.
repository: tanstack/query
label: Concurrency
language: Markdown
comments_count: 4
repository_stars: 49380
---

When using async/concurrent flows (streaming, dehydration/rehydration, optimistic updates), ensure you never persist “in-flight” async state and you always return promises from async callbacks.

1) Don’t persist promises during streaming/dehydration
- If a query might still be pending, configuring persistence to store only settled/resolved outcomes prevents serialization issues when pending work is dehydrated and streamed.

```tsx
<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,
    // Persist only queries that have resolved (not pending promises)
    dehydrateOptions: { shouldDehydrateQuery: defaultShouldDehydrateQuery },
  }}
>
  {children}
</PersistQueryClientProvider>
```

2) Don’t drop promise lifecycles in concurrency callbacks
- For concurrency-related callback hooks (e.g., mutation lifecycle handlers) that trigger async work, write them in a way that returns the promise (consistent concise arrow syntax is preferred).

```ts
useMutation({
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});
```

Practical checklist:
- Any persistence/dehydration layer: allow only resolved/errored (settled) query results to be stored.
- Any callback that triggers async operations: return the promise so downstream orchestration/lifecycle expectations remain correct.