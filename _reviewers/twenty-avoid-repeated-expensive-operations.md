---
title: Avoid repeated expensive operations
description: Replace repeated expensive operations like `find()`, `filter()`, or `sort()`
  with pre-computed maps or cached results to improve performance. When the same lookup
  or computation is performed multiple times, create a map or dictionary for O(1)
  access instead of O(n) searches.
repository: twentyhq/twenty
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 35477
---

Replace repeated expensive operations like `find()`, `filter()`, or `sort()` with pre-computed maps or cached results to improve performance. When the same lookup or computation is performed multiple times, create a map or dictionary for O(1) access instead of O(n) searches.

**Examples of optimization:**

Instead of repeated `find()` calls:
```javascript
// ❌ Inefficient - O(n) lookup each time
const handlePointClick = (point) => {
  const series = data.find((s) => s.id === point.seriesId);
  // ... later in code
  const anotherSeries = data.find((s) => s.id === otherId);
};

// ✅ Efficient - O(1) lookup with pre-computed map
const dataMap = useMemo(() => 
  data.reduce((map, item) => ({ ...map, [item.id]: item }), {}), 
  [data]
);

const handlePointClick = (point) => {
  const series = dataMap[point.seriesId];
  // ... later in code
  const anotherSeries = dataMap[otherId];
};
```

Instead of repeated sorting:
```javascript
// ❌ Inefficient - sorting already sorted data
const actionsToRegister = Object.values(actionConfig ?? {})
  .filter((action) => action.availableOn?.includes(viewType))
  .sort((a, b) => a.position - b.position);

// ✅ Efficient - pre-sort the configuration
const sortedActionConfig = useMemo(() => 
  Object.values(actionConfig ?? {}).sort((a, b) => a.position - b.position),
  [actionConfig]
);
```

This optimization is particularly important in render loops, event handlers, and frequently called functions where the same expensive operations are performed repeatedly.