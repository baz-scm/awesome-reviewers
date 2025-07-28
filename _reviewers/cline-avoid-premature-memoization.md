---
title: Avoid premature memoization
description: Don't automatically reach for useMemo and useCallback for every computation
  or function. These hooks add complexity and should only be used when there's a measurable
  performance benefit. Consider the actual cost of the operation and frequency of
  re-renders before memoizing.
repository: cline/cline
label: React
language: TSX
comments_count: 2
repository_stars: 48299
---

Don't automatically reach for useMemo and useCallback for every computation or function. These hooks add complexity and should only be used when there's a measurable performance benefit. Consider the actual cost of the operation and frequency of re-renders before memoizing.

Use memoization when:
- The computation is expensive (complex calculations, object creation)
- The component re-renders frequently 
- Dependencies change infrequently

Avoid memoization for:
- Simple calculations or lightweight operations
- Operations that run once or rarely
- When the "optimization" is more complex than the original code

Example of appropriate memoization:
```tsx
// Good: Component re-renders frequently, URL construction has dependencies
const clineUris = useMemo(() => {
  const base = new URL(clineUser?.appBaseUrl || CLINE_APP_URL)
  const dashboard = new URL("dashboard", base)
  const credits = new URL(activeOrganization ? "/organization" : "/account", dashboard)
  credits.searchParams.set("tab", "credits")
  return { dashboard, credits }
}, [clineUser?.appBaseUrl, activeOrganization])
```

Remember: "Premature optimization is the root of all evil." Profile first, optimize second.