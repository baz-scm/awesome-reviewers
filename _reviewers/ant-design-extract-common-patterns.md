---
title: Extract common patterns
description: When you encounter repeated code patterns, conditional logic within loops,
  or similar implementations across components, extract them into reusable utilities
  or common styles. This improves maintainability, reduces bundle size, and makes
  the codebase more consistent.
repository: ant-design/ant-design
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 95882
---

When you encounter repeated code patterns, conditional logic within loops, or similar implementations across components, extract them into reusable utilities or common styles. This improves maintainability, reduces bundle size, and makes the codebase more consistent.

Key practices:
- Extract repeated styles into common utilities (e.g., blur effects, reset functions)
- Remove conditional checks from loops by handling special cases separately
- Flatten function parameters instead of using object destructuring to reduce bundle size
- Use direct comparisons instead of array methods like `includes()` for simple checks
- Choose implementation approaches that support future extensibility

Example:
```typescript
// Instead of conditional logic in loop:
items.forEach(item => {
  if (item.type === 'special') {
    // special handling
  }
  // regular processing
});

// Extract special cases:
const specialItems = items.filter(item => item.type === 'special');
const regularItems = items.filter(item => item.type !== 'special');
specialItems.forEach(handleSpecialItem);
regularItems.forEach(handleRegularItem);
```

This approach makes code more readable, testable, and often results in better performance and smaller bundle sizes.