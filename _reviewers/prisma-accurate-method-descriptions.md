---
title: Accurate method descriptions
description: API documentation must precisely describe method behavior, especially
  return values and cardinality. Inaccurate descriptions mislead developers about
  what methods actually return, potentially causing runtime errors or incorrect assumptions.
repository: prisma/prisma
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 42967
---

API documentation must precisely describe method behavior, especially return values and cardinality. Inaccurate descriptions mislead developers about what methods actually return, potentially causing runtime errors or incorrect assumptions.

Key areas to verify:
- **Return value nullability**: Clearly state when methods can return null/undefined
- **Result cardinality**: Use precise language like "zero or one" vs "one", or "zero or more" vs "one or more"
- **Actual behavior alignment**: Ensure descriptions match the method's real implementation

Example of incorrect vs correct documentation:

```javascript
// ❌ Incorrect - misleading about nullability
/**
 * Find one User that matches the filter.
 */
findUnique(args) { ... }

// ✅ Correct - accurate about possible null return
/**
 * Returns User that matches the filter or `null` if nothing is found.
 */
findUnique(args) { ... }

// ❌ Incorrect - wrong cardinality
/**
 * Find one or more Users that matches the filter.
 */
findMany(args) { ... }

// ✅ Correct - accurate cardinality
/**
 * Find zero or more Users that matches the filter.
 */
findMany(args) { ... }
```

This prevents developers from making incorrect assumptions about method behavior and reduces debugging time caused by unexpected null values or empty results.