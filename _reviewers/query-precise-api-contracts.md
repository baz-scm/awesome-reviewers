---
title: Precise API Contracts
description: 'When designing or documenting API options and callbacks, ensure the
  contract is exact, unambiguous, and type-safe.


  - **Specify true behavior and defaults**: If an option affects multiple behaviors,
  document what it does *exactly* (including defaults). Prefer the control mechanism
  that precisely matches intent (e.g., stop polling by returning `false` from...'
repository: tanstack/query
label: API
language: Markdown
comments_count: 7
repository_stars: 49380
---

When designing or documenting API options and callbacks, ensure the contract is exact, unambiguous, and type-safe.

- **Specify true behavior and defaults**: If an option affects multiple behaviors, document what it does *exactly* (including defaults). Prefer the control mechanism that precisely matches intent (e.g., stop polling by returning `false` from `refetchInterval`, not by disabling the query if that impacts more than polling).
- **Make TypeScript reflect reality**: Export/extract the correct public types, and ensure required/optional fields match current behavior (e.g., don’t claim `mutationKey` is required if it isn’t). Use narrower option types for wrappers (so unsupported options are rejected by TS rather than silently ignored).
- **Avoid concept/name collisions**: If different parts of the API use the same term (like multiple “context” meanings), either rename one concept or clearly distinguish them in docs and examples (optionally via a more explicit name like “scope”).
- **Document cross-runtime input constraints**: For SSR/server-action boundaries, ensure inputs are serializable; don’t pass function references as `queryFn` where only serializable values are allowed—call functions so arguments are safe.

Example (control-flow precision):
```ts
useQuery({
  queryKey: ['job', jobId],
  queryFn: () => fetchJobStatus(jobId),
  refetchInterval: (query) => {
    if (query.state.data?.status === 'complete') return false
    return 2000
  },
})
```