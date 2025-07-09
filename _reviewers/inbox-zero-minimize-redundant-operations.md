---
title: Minimize redundant operations
description: Optimize application performance by preventing unnecessary renders, calculations,
  and network operations. Implement proper memoization strategies, lift shared operations
  to parent components, and batch related tasks.
repository: elie222/inbox-zero
label: Performance Optimization
language: TSX
comments_count: 6
repository_stars: 8267
---

Optimize application performance by preventing unnecessary renders, calculations, and network operations. Implement proper memoization strategies, lift shared operations to parent components, and batch related tasks.

**Memoization best practices:**
- Ensure comparison functions in `memo()` accurately evaluate prop changes:
```jsx
// Incorrect: Always returns true, preventing needed updates
export const Component = memo(PureComponent, () => true);

// Correct: Uses default shallow comparison or provides accurate comparison
export const Component = memo(PureComponent);
// Or with custom comparison when needed:
export const Component = memo(PureComponent, (prev, next) => 
  prev.id === next.id && prev.status === next.status
);
```

**Data operations:**
- Move shared hooks and state to parent components instead of repeating in list items
- Batch related network calls and updates with Promise.all:
```jsx
// Inefficient: Serial execution with multiple updates
const handleBulkOperation = async () => {
  for (const id of selected) {
    await apiCall(id);  // N network requests
    mutate();           // N re-validations
  }
};

// Optimized: Parallel execution with single update
const handleBulkOperation = async () => {
  const calls = selected.map(id => apiCall(id));
  await Promise.all(calls);  // Parallel requests
  mutate();                  // Single re-validation
};
```

**Expensive calculations:**
- Extract expensive calculations into memoized functions with useMemo or into callbacks that execute only when needed, not on every render