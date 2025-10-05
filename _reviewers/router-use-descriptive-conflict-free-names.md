---
title: Use descriptive, conflict-free names
description: Choose descriptive names that clearly convey purpose while avoiding conflicts
  with existing APIs, built-in functions, or established conventions. Names should
  follow consistent patterns across the codebase and use appropriate spelling conventions.
repository: TanStack/router
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 11590
---

Choose descriptive names that clearly convey purpose while avoiding conflicts with existing APIs, built-in functions, or established conventions. Names should follow consistent patterns across the codebase and use appropriate spelling conventions.

Key principles:
- Prefer descriptive names over abbreviated ones (e.g., `dehydratedRouter` instead of `r`)
- Avoid conflicts with built-in functions (e.g., `fetchAndResolveInLoaderLifetime` instead of `fetch`)
- Don't clash with framework conventions (e.g., `getSupabaseServer` instead of `useSupabase` for non-hooks)
- Follow established naming patterns in the codebase (e.g., `disableManifestGeneration` to match `disableTypes`)
- Use consistent spelling conventions (e.g., US spelling: `behavior` not `behaviour`)
- Choose meaningful variable names that reflect their content (e.g., `derived` instead of `paths`)

Example:
```typescript
// ❌ Avoid: Abbreviated, conflicts with built-in
const r = getRouter()
const fetch = async () => { ... }

// ✅ Good: Descriptive, conflict-free
const dehydratedRouter = getRouter()
const fetchAndResolveInLoaderLifetime = async () => { ... }

// ❌ Avoid: Misleading naming pattern
export function useSupabase() { /* not a hook */ }

// ✅ Good: Clear, follows conventions
export function getSupabaseServer() { /* server utility */ }
```