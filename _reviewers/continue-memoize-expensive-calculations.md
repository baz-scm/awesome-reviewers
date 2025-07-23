---
title: Memoize expensive calculations
description: 'Cache computation results in React components to prevent unnecessary
  recalculations during re-renders, which can significantly impact application performance.
  Apply these optimization techniques in three key areas:'
repository: continuedev/continue
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 27819
---

Cache computation results in React components to prevent unnecessary recalculations during re-renders, which can significantly impact application performance. Apply these optimization techniques in three key areas:

1. **Redux selectors**: Ensure selectors return stable references or use memoization libraries like reselect:
```tsx
// Suboptimal approach
const currentToolCall = useAppSelector(selectCurrentToolCall);

// Optimized approach
import { createSelector } from 'reselect';
const memoizedSelector = createSelector(
  [selectCurrentToolCall],
  (toolCall) => toolCall
);
const currentToolCall = useAppSelector(memoizedSelector);
```

2. **Expensive calculations**: Move computations with O(n) or higher complexity outside render loops and cache them:
```tsx
// Suboptimal approach - O(n²) complexity
{history.map(item => {
  const latestSummaryIndex = findLatestSummaryIndex(history);
  // rest of render logic
})}

// Optimized approach - O(n) complexity
const latestSummaryIndex = useMemo(() => 
  findLatestSummaryIndex(history), 
  [history]
);
{history.map(item => {
  // use latestSummaryIndex
  // rest of render logic
})}
```

3. **Frequently called functions**: Extract calculations into custom hooks or memoize them to prevent recalculation on every render:
```tsx
// Suboptimal approach
<div style={{ fontSize: getFontSize() }}>

// Optimized approach
const fontSize = useFontSize();
<div style={{ fontSize }}>
```

When implementing these optimizations, focus on functions that perform expensive calculations or create new object references, especially those called frequently during renders or within loops.