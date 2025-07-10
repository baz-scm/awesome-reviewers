---
title: Memoize expensive computations effectively
description: Prevent unnecessary recalculations and rerenders by properly memoizing
  expensive computations and derived values in React components. Pay special attention
  to dependency arrays and ensure they only include stable references.
repository: getsentry/sentry
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 41297
---

Prevent unnecessary recalculations and rerenders by properly memoizing expensive computations and derived values in React components. Pay special attention to dependency arrays and ensure they only include stable references.

Key points:
- Memoize derived values that depend on props or state
- Avoid using objects or arrays directly in dependency arrays
- Be particularly careful with router-related objects like searchParams that create new references

Example of proper memoization:
```typescript
// Instead of this (causes unnecessary recalculations):
const sortBysString = JSON.stringify(sortBys);

// Do this:
const sortBysString = useMemo(() => JSON.stringify(sortBys), [sortBys]);

// For functions that depend on changing objects, extract stable values:
const handleSearchChange = useMemo(
  () =>
    debounce((newValue: string) => {
      const currentParams = Object.fromEntries(searchParams.entries());
      // ... rest of the logic
    }, 500),
  [setSearchParams] // Only depend on stable function reference
);
```

This optimization is particularly important for:
- JSON operations
- String manipulations
- Debounced/throttled function creation
- Derived calculations from props/state