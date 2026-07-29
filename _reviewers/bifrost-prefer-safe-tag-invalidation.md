---
title: Prefer safe tag invalidation
description: When a server mutation (e.g., model discovery refresh) changes data that
  feeds multiple cached selectors/queries, use RTK Query tag invalidation to refresh
  all dependent caches—especially indirect ones.
repository: maximhq/bifrost
label: Caching
language: TypeScript
comments_count: 2
repository_stars: 6862
---

When a server mutation (e.g., model discovery refresh) changes data that feeds multiple cached selectors/queries, use RTK Query tag invalidation to refresh all dependent caches—especially indirect ones.

Guideline
- Invalidate every cache tag type that can become stale due to the mutation (not just the primary entity).
- If the mutation response can’t be cleanly mapped into the existing cached query shape(s), prefer invalidation over patching to avoid subtle shape-mismatch bugs.
- Invalidate provider-scoped entries as well, so list/detail views (and any key/model pickers) update consistently.

Example (pattern)
```ts
const refreshProviderModels = builder.mutation<ModelProviderKey[], string>({
  query: (provider) => ({
    url: `/providers/${encodeURIComponent(provider)}/refresh-models`,
    method: 'POST',
  }),
  invalidatesTags: [
    'Models',
    'DBKeys',
    { type: 'Providers' as const, id: provider },
  ],
});
```

Application checklist
- Identify what the refresh rewrites on the backend (e.g., per-key `models`) and which UI components depend on it.
- Add corresponding tag types to `invalidatesTags` for those dependencies.
- Avoid complex `updateQueryData`/patching unless the response can be mapped losslessly to the cached query’s existing item shape.