---
title: Use semantic naming
description: Choose semantic, logical names that describe purpose and intent rather
  than physical characteristics or implementation details. This improves code maintainability,
  internationalization support, and clarity.
repository: facebook/yoga
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 18255
---

Choose semantic, logical names that describe purpose and intent rather than physical characteristics or implementation details. This improves code maintainability, internationalization support, and clarity.

For CSS properties, prefer logical properties over directional ones:
```typescript
// Instead of physical directions
'margin-left', 'margin-right'

// Use logical directions  
'margin-inline-start', 'margin-inline-end'
'inset-inline-start', 'inset-inline-end'
```

For API parameters and types, use precise, descriptive names that clearly communicate expected values:
```typescript
// Instead of generic types
setMargin(edge: Edge, margin: number | string): void

// Use specific, semantic types
setMargin(edge: Edge, margin: number | 'auto' | `${number}%`): void
```

This approach creates more robust, internationally-friendly code that better expresses developer intent and reduces ambiguity about expected values or behavior.