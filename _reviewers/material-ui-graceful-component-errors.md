---
title: Graceful component errors
description: Use descriptive error messages and appropriate error severity based on
  component maturity and usage patterns. For newer components, throwing errors is
  acceptable when constraints are violated. For established components, consider using
  development-mode warnings instead of throwing errors to avoid breaking existing
  implementations.
repository: mui/material-ui
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 96063
---

Use descriptive error messages and appropriate error severity based on component maturity and usage patterns. For newer components, throwing errors is acceptable when constraints are violated. For established components, consider using development-mode warnings instead of throwing errors to avoid breaking existing implementations.

**When writing error messages:**
- Be specific about the relationship between components
- Clearly state what the developer needs to do to fix the issue

**When deciding error severity:**
- Consider how the component might be used in the wild
- Be more conservative with established components

Example:
```typescript
// Better error message
if (ctx === null) {
  if (process.env.NODE_ENV !== 'production') {
    console.warn('Material UI: The Tab component should be used inside a Tabs component');
  }
  // Provide fallback behavior if possible
  return defaultContext;
}

// Instead of throwing:
if (ctx === null) {
  throw new Error('Material UI: Tabs component was not found in the tree');
}
```

This approach balances between guiding developers toward correct usage while maintaining compatibility with existing code that might use components in unexpected ways.