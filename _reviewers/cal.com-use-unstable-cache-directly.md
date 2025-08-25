---
title: Use unstable_cache directly
description: When implementing server-side caching in Next.js applications, prefer
  using `unstable_cache` with direct repository method calls instead of tRPC callers.
  This approach provides better performance and proper integration with Next.js caching
  mechanisms.
repository: calcom/cal.com
label: Caching
language: TSX
comments_count: 2
repository_stars: 37732
---

When implementing server-side caching in Next.js applications, prefer using `unstable_cache` with direct repository method calls instead of tRPC callers. This approach provides better performance and proper integration with Next.js caching mechanisms.

Instead of using tRPC callers for cached data:
```ts
const caller = await createRouterCaller(workflowsRouter);
const initialData = await caller.filteredList({ filters });
```

Use `unstable_cache` directly with repository methods:
```ts
const getWorkflowsFilteredListCached = unstable_cache(
  async (filters) => { // filters should be serializable
    return await WorkflowRepository.getFilteredList(filters);
  },
  ["getWorkflowsFilteredListCached"],
  {
    revalidate: 3600,
    tags: ["viewer.workflows.filteredList"]
  }
);

const initialData = await getWorkflowsFilteredListCached(filters);
```

This pattern enables proper cache revalidation using `revalidateTag` from `next/cache` in CRUD operations and eliminates unnecessary tRPC overhead for cached operations. Apply this consistently across server components where data caching is needed.