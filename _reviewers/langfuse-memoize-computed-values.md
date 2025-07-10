---
title: Memoize computed values
description: Cache the results of expensive operations and component renders to avoid
  redundant calculations during re-renders. This improves application performance,
  especially when working with large datasets or complex transformations.
repository: langfuse/langfuse
label: Performance Optimization
language: TSX
comments_count: 5
repository_stars: 13574
---

Cache the results of expensive operations and component renders to avoid redundant calculations during re-renders. This improves application performance, especially when working with large datasets or complex transformations.

**Key practices:**

1. Use `React.useMemo()` for derived data transformations:
```jsx
// Instead of this:
const renderedData = data.map((item) => {
  // expensive transformation
});

// Do this:
const renderedData = React.useMemo(() => {
  return data.map((item) => {
    // expensive transformation
  });
}, [data]);
```

2. Implement complete comparison functions in `React.memo()`:
```jsx
// Incorrect - incomplete prop comparison
const MemoComponent = React.memo(Component, (prev, next) => {
  return prev.id === next.id; // Missing comparison of other props
});

// Correct - comprehensive comparison
const MemoComponent = React.memo(Component, (prev, next) => {
  return prev.id === next.id && prev.data === next.data;
});
```

3. Cache intermediate results to avoid repeated expensive operations:
```jsx
// Instead of parsing multiple times:
const parsedData = JSON.parse(rawData);
const filteredItems = items.filter(item => {
  const parsed = JSON.parse(rawData); // Redundant parsing
  return parsed.id === item.id;
});

// Parse once and reuse:
const parsedData = JSON.parse(rawData);
const filteredItems = items.filter(item => parsedData.id === item.id);
```

4. Pre-compute values used in filtering operations:
```jsx
// Instead of mapping inside filter:
const validScores = scores.filter(scoreId => 
  allScores.data?.scores.map(s => s.id).includes(scoreId)
);

// Pre-compute the lookup list:
const scoreIdSet = new Set(allScores.data?.scores.map(s => s.id));
const validScores = scores.filter(scoreId => scoreIdSet.has(scoreId));
```

Proper memoization prevents unnecessary recalculations and renders, significantly improving performance for data-intensive applications.