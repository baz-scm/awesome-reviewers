---
title: API typing parity
description: When evolving public API/TypeScript types, ensure the **type surface
  exactly matches runtime behavior and intended layering**, and reuse existing signature/overload
  patterns.
repository: tanstack/query
label: API
language: TypeScript
comments_count: 10
repository_stars: 49380
---

When evolving public API/TypeScript types, ensure the **type surface exactly matches runtime behavior and intended layering**, and reuse existing signature/overload patterns.

Practical rules:
1) **Parity for accepted shapes**: If the runtime supports multiple input forms (e.g. `ref`, `computed`, `() => value`), the exported types must accept the same set.
2) **Mirror established method patterns**: New methods should match the signature style of analogous APIs (e.g. `fetchQuery`/`useQuery`): same overload structure, same options interface, and consistent generic parameter order.
3) **Correct abstraction layer**: Don’t add an option to the wrong type (query vs observer). If behavior is observer-specific, it must live in observer-level options/types.
4) **Migration via deprecated overloads**: If v5 changes argument shape (object-only, etc.), provide a deprecated overload for old calling conventions rather than silently breaking.
5) **Explicit precedence for conflicting inputs**: When two options can interact (e.g. `skipToken` + `enabled`), define the precedence in both runtime and types so users can’t form contradictory combinations.
6) **Avoid misleading widening**: Don’t widen public event/action types in a way that implies users can subscribe/receive things that can’t actually occur through the supported mechanism.

Example (pattern for migration + deprecation):
```ts
// preferred v5 style
find(filters: QueryFilters): Query | undefined

/** @deprecated Use the single-object overload instead */
find(queryKey: QueryKey, filters?: OmitKeyof<QueryFilters, 'queryKey'>): Query | undefined
```

Example (precedence):
- If `enabled: true` must override `queryFn: skipToken`, encode that rule (and ideally prevent passing both in types via overloads/unions).

These checks prevent subtle regressions where developers rely on types to describe reality—especially for reactive/getter inputs, options placement, and overload/migration paths.