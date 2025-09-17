---
title: Ensure semantic precision
description: Choose names and identifiers that precisely convey their intended semantic
  meaning and avoid ambiguity or conflicts. Names should be specific enough to prevent
  confusion and clearly communicate their purpose within the codebase.
repository: unionlabs/union
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 74800
---

Choose names and identifiers that precisely convey their intended semantic meaning and avoid ambiguity or conflicts. Names should be specific enough to prevent confusion and clearly communicate their purpose within the codebase.

For type definitions, prefer semantically precise types over generic ones when the distinction matters. For example, use `{}` (explicitly empty object) rather than `object` when you specifically need an empty type:

```typescript
export type SwitchChainState = Data.TaggedEnum<{
  InProgress: {} // Explicitly empty, not just any object
}>
```

For class and tag names, ensure uniqueness across the application by using descriptive prefixes or suffixes when necessary:

```typescript
// Instead of generic names that might conflict
export class SuiPublicClientSource extends Context.Tag("SuiPublicClientSource")
export class SuiPublicClientDestination extends Context.Tag("SuiPublicClientDestination")
```

This practice prevents naming conflicts, reduces cognitive load when reading code, and makes the codebase more maintainable by ensuring each identifier has a clear, unambiguous meaning.