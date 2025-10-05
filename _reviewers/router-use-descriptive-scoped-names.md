---
title: Use descriptive scoped names
description: Prefer descriptive, scoped names over generic or vague identifiers for
  types, functions, and properties. Names should clearly communicate their purpose
  and context within the codebase.
repository: TanStack/router
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 11590
---

Prefer descriptive, scoped names over generic or vague identifiers for types, functions, and properties. Names should clearly communicate their purpose and context within the codebase.

For boolean properties, consider using getter functions with descriptive names instead of direct property access:
```ts
// Instead of direct property access
isClosed: boolean

// Consider descriptive getter
getIsClosedStatus(): boolean
```

For types, use specific, scoped names rather than generic ones:
```ts
// Too generic
type Resolver = { ... }

// More descriptive and scoped  
type BlockerFnResolver = { ... }
type BlockerResolver = { ... }
```

For object structures, maintain consistent naming patterns that support future extensibility:
```ts
// Structured approach that supports extension
export type MyRouterContext = {
  auth: AuthContextType
  // Easy to add: query: QueryContextType
}
```

This approach improves code readability, reduces ambiguity, and makes the codebase more maintainable by clearly communicating the intent and scope of each identifier.