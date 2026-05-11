---
title: Type-safe option consistency
description: Typed “options” objects (e.g. `queryOptions`, `infiniteQueryOptions`,
  `mutationOptions`) should round-trip cleanly across *all* API entrypoints that accept
  them (hooks, suspense/non-suspense hooks, and `QueryClient` methods).
repository: tanstack/query
label: API
language: TSX
comments_count: 4
repository_stars: 49380
---

Typed “options” objects (e.g. `queryOptions`, `infiniteQueryOptions`, `mutationOptions`) should round-trip cleanly across *all* API entrypoints that accept them (hooks, suspense/non-suspense hooks, and `QueryClient` methods).

**Standard**
1. **Assignability invariant:** Any object returned by a `*Options` factory must be assignable to every corresponding `Use*Options` / client/method parameter type without requiring userland type assertions.
2. **Transformation propagation:** If an option supports a transformation callback (e.g. `select`), the callback’s return type must be preserved identically across every entrypoint that consumes that option.
3. **Ergonomic typing helpers:** When advanced generic composition is needed (reusable wrappers), export `Any*` utility types (e.g. `AnyUseQueryOptions`) so consumers can write correct generic helpers without brittle casts or excessive type parameters.
4. **Enforce with type tests:** Add `*.test-d.tsx` coverage for (a) passing the same options object into each entrypoint, and (b) verifying `select`/transformed data types.

**Example (what to ensure)**
```ts
const options = infiniteQueryOptions({
  queryKey: ['key'],
  queryFn: () => Promise.resolve('string'),
  getNextPageParam: () => 1,
  initialPageParam: 1,
  select: (data) => data.pages, // transformed type
})

// Should compile with identical transformed output types:
const a = useSuspenseInfiniteQuery(options)
const b = await new QueryClient().infiniteQuery(options)

// Team rule: both should infer the same selected/transformed type.
```

Apply this when evolving API types: if a change fixes typing for one entrypoint (e.g. `useInfiniteQuery`) it must be validated for the client methods and suspense variants too.