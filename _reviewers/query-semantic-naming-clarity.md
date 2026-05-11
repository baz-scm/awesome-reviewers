---
title: Semantic naming clarity
description: When introducing names for APIs/docs and for contribution metadata, ensure
  the naming is semantic and cannot be mistaken for a requirement that isn’t real.
repository: tanstack/query
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 49380
---

When introducing names for APIs/docs and for contribution metadata, ensure the naming is semantic and cannot be mistaken for a requirement that isn’t real.

**Apply this rule**
1) **Avoid misleading implied constraints**: If two keys/identifiers are shown together, make it explicit whether they *must* match or are simply examples.
2) **Prefer domain-based, unambiguous identifiers**: Name commit scopes by library/framework area (e.g., `react-query`, `query-core`) rather than narrowly duplicated code-level terms.
3) **Use the team/standard vocabulary for commit types**: Only use commit type labels that match the accepted conventional-commit configuration (e.g., `types` only if it’s allowed by your commitlint rules).

**Example (docs/config helper)**
```ts
function groupMutationOptions() {
  return mutationOptions({
    mutationKey: ['groups'], // required: identifies the mutation
    mutationFn: addGroup,
    // Note: mutationKey does NOT need to equal the queryKey used by the invalidation.
  })
}

useMutation({
  ...groupMutationOptions(),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['groups'] }),
})
```

**Example (commit scope/type naming)**
- Prefer: `types(react-query): add mutationOptions typing support`
- Prefer: `chore(query-core): update build tooling`
- Avoid scopes like `useQuery` if they can be duplicated across adapters; prefer the library/framework area instead.