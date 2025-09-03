---
title: avoid inline object creation
description: Inline objects and functions created within render methods are recreated
  on every render, causing unnecessary re-renders of child components when passed
  as props. This impacts performance by triggering component updates even when the
  actual functionality hasn't changed.
repository: SigNoz/signoz
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 23369
---

Inline objects and functions created within render methods are recreated on every render, causing unnecessary re-renders of child components when passed as props. This impacts performance by triggering component updates even when the actual functionality hasn't changed.

To optimize performance, extract inline objects and functions using memoization techniques:

- Use `useCallback` for inline functions
- Use `useMemo` for inline objects
- Extract static objects outside the component

Example of the problem:
```tsx
// Problematic - creates new object on every render
<Table
  locale={{
    emptyText: 'No data available'
  }}
/>

// Optimized - memoize the object
const tableLocale = useMemo(() => ({
  emptyText: 'No data available'
}), []);

<Table locale={tableLocale} />
```

This practice prevents unnecessary child component re-renders and improves overall application performance.