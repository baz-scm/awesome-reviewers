---
title: Semantic naming consistency
description: 'Use names that match the value’s real meaning and align with established/public
  API conventions.


  Practical rules:

  - **Name by semantics, not by adjacent intuition**: if “context” is being reinterpreted,
  rename (and deprecate old names with clear JSDoc) rather than silently changing
  what the term means.'
repository: tanstack/query
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 49380
---

Use names that match the value’s real meaning and align with established/public API conventions.

Practical rules:
- **Name by semantics, not by adjacent intuition**: if “context” is being reinterpreted, rename (and deprecate old names with clear JSDoc) rather than silently changing what the term means.
- **Match existing public API / adapter conventions**: if the library exposes `setQueries(queries)` and callers already use “queries”, keep internal variables consistent (even if “options” feels more precise).
- **Use framework/runtime signaling in names**: in Angular, functions that rely on an injection context should be clearly marked (e.g., prefer `injectX` when using `inject(...)`).
- **Match prop/example naming**: prefer `client` vs `queryClient` when it mirrors `QueryClientProvider client={...}` and the corresponding destructuring examples.
- **Signal API stability explicitly**: new experimental/unstable additions should include `experimental_`/`unstable_` in the name when that’s the project’s convention.
- **Avoid ambiguous plural/generic terms**: if a field implies a specific contract (e.g., fetching multiple pages), choose names that help enforce/communicate the required pairing.

Examples:
```ts
// Semantic rename with deprecation
export interface MutationState<TData, TError, TVariables, TScope = unknown> {
  /** @deprecated Use `scope` instead. */
  context: TScope | undefined
  scope: TScope | undefined
}

// Keep naming consistent with public API
// useQueries({ queries }) ... setQueries(queries)
const defaultedQueries = /* keep `queries` naming */

// Angular injection-context signaling
export function injectIsFetching(filters?: QueryFilters, queryClient?: QueryClient) {
  // uses `inject(...)` internally; name reflects requirement
}

// Provider-aligned naming
useQuery({
  queryKey,
  queryFn: ({ client, signal }) => {/* ... */},
})

// Stability signaling
experimental_promise: Promise<TData>
```