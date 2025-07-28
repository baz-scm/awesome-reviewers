---
title: Use descriptive names
description: Choose variable, function, and file names that clearly describe their
  purpose, behavior, and content. Names should be self-documenting and avoid ambiguity
  about what they represent or do.
repository: nuxt/nuxt
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 57769
---

Choose variable, function, and file names that clearly describe their purpose, behavior, and content. Names should be self-documenting and avoid ambiguity about what they represent or do.

Key principles:
- **Reflect actual behavior**: Use names that accurately describe what the code does, not just what it might do. For example, `hasIntersected` instead of `isIntersecting` when the value doesn't toggle back to false.
- **Be specific and clear**: Prefer `shared-imports.d.ts` over `shared.d.ts`, or `cookieStore` over `listenCookieChanges` to identify the specific API being used.
- **Use inclusive language**: Replace terms like `whitelist` with `allowlist` to maintain inclusive terminology.
- **Choose semantic function names**: Use `shouldPrefetch()` instead of `checkShouldPrefetch()` when the function returns a boolean indicating whether an action should be performed.

Example of good descriptive naming:
```typescript
// Before: unclear behavior
const isIntersecting = ref(false)
function checkShouldPrefetch() { /* ... */ }

// After: clear and descriptive  
const hasIntersected = ref(false)
function shouldPrefetch(): boolean { /* ... */ }

// Before: generic naming
whitelist: string[]

// After: descriptive and inclusive
allowlist: string[]
```

This approach makes code more maintainable and reduces the need for additional documentation or comments to explain what identifiers represent.