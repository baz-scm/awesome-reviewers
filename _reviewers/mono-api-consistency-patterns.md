---
title: API consistency patterns
description: Maintain consistent patterns across similar APIs to improve developer
  experience and reduce cognitive overhead. When designing related APIs, use factory
  patterns for shared contexts, consistent parameter structures, and uniform return
  types.
repository: rocicorp/mono
label: API
language: TypeScript
comments_count: 5
repository_stars: 2091
---

Maintain consistent patterns across similar APIs to improve developer experience and reduce cognitive overhead. When designing related APIs, use factory patterns for shared contexts, consistent parameter structures, and uniform return types.

Key principles:
- Use factory patterns to eliminate repetitive context definitions
- Prefer object parameters over multiple positional arguments for better extensibility
- Structure return types consistently across similar functions
- Place related methods on the same object for logical grouping

Example of factory pattern for shared context:
```ts
// Instead of repeating auth context everywhere
const { syncedQueryWithContext } = createQueriesWithContextFactory<AuthData>()

syncedQueryWithContext(
  'user',
  validator.parse,
  // Automatically typed as AuthData | undefined
  (auth, userID) => {}
)
```

Example of consistent return structure:
```ts
// Return structured data consistently
type QueryResult<TReturn> = readonly [
  Smash<TReturn>,
  QueryResultDetails,
];

// Instead of mixed return types
function useQuery(): Accessor<QueryResult<TReturn>>
```

Example of object parameters:
```ts
// Prefer object parameters for extensibility
mutator(args: {
  arg1?: string;
  arg2?: string;
});

// Over positional arguments that are rigid
mutator(arg1?: string, arg2?: string)
```