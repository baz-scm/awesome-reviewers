---
title: Explicit undefined invariants
description: When handling query/mutation results, treat `undefined` (and `null`)
  as semantically distinct and enforce that distinction in both runtime checks and
  TypeScript types.
repository: tanstack/query
label: Null Handling
language: TypeScript
comments_count: 10
repository_stars: 49380
---

When handling query/mutation results, treat `undefined` (and `null`) as semantically distinct and enforce that distinction in both runtime checks and TypeScript types.

**Coding standards**
1. **Never use truthy checks for cached/data presence.**
   - Use explicit comparisons so valid falsy values (`null`, `false`, `""`) are not misclassified.
   - Prefer:
     - `value !== undefined` / `value === undefined`
2. **Do not resolve/return `undefined` where the API contract says it can’t.**
   - Avoid non-null assertions (`!`) that hide cancelled/empty states.
   - Add explicit branches for “cancelled/skip” paths.
3. **For “skip”/sentinel control tokens, don’t treat them as normal data that returns `undefined`.**
   - Prefer rejecting/throwing (or preventing execution) so that the invariant is preserved.
4. **Align types with runtime: encode “undefined not allowed” in generics, and avoid type-widening fallbacks.**
   - Prefer precise `undefined`/optional handling over `{}`-style fallbacks that widen unions.

**Example**
```ts
// 1) Presence checks: don’t use truthy
const data = query.state.data
const hasData = data !== undefined // null/false/"" are valid

// 2) Imperative fetch contract: never resolve undefined
async function fetchQueryImperative() {
  if (initialFetchCancelled) {
    throw new Error('Cancelled')
  }
  // safe: data is guaranteed by control flow
  return data
}

// 3) Skip token: don’t return undefined as “success data”
if (queryFn === skipToken) {
  return Promise.reject(
    new Error('Attempted to invoke queryFn when set to skipToken')
  )
}
```

Applying these rules prevents subtle SSR/hydration mismatches, avoids incorrect cache restore decisions, and keeps null/undefined behavior predictable across the codebase.