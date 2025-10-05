---
title: validate before accessing
description: Always validate that values exist and have expected properties before
  accessing them, especially when removing non-null assertions or performing type
  casting. Avoid making assumptions about value presence or type safety without explicit
  checks.
repository: TanStack/router
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 11590
---

Always validate that values exist and have expected properties before accessing them, especially when removing non-null assertions or performing type casting. Avoid making assumptions about value presence or type safety without explicit checks.

Key practices:
- When removing non-null assertion operators (!), add explicit null/undefined checks
- Validate input types before casting, especially with schema validation libraries
- Use specific filtering logic instead of generic Boolean filtering that may exclude valid falsy values
- Consider whether to pass empty objects vs undefined parameters based on actual usage

Example from the discussions:
```typescript
// Risky - assumes route exists after removing non-null assertion
const route = this.looseRoutesById[d.routeId]

// Better - validate before use
const route = this.looseRoutesById[d.routeId]
if (!route) return

// Risky - Boolean filter excludes valid falsy numbers like 0, -1
paths.filter(Boolean).join('/')

// Better - explicit check for meaningful values
paths.filter((val) => val !== undefined && val !== null).join('/')
```

This prevents runtime errors from null reference exceptions and ensures code behaves correctly with edge case values.