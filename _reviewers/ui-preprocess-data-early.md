---
title: Preprocess data early
description: Transform and prepare data structures at their source rather than during
  consumption. This includes flattening nested objects, sorting collections, and other
  manipulations that make data more efficient to process downstream.
repository: shadcn-ui/ui
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 90568
---

Transform and prepare data structures at their source rather than during consumption. This includes flattening nested objects, sorting collections, and other manipulations that make data more efficient to process downstream.

When working with nested structures like configuration objects, flatten them early:

```javascript
// Instead of:
function processColors(colors) {
  return typeof colors === "string" ? { [name]: colors } : colors;
  // This doesn't handle deeply nested color objects properly
}

// Prefer:
function processColors(colors) {
  return typeof colors === "string" ? { [name]: colors } : flatten(colors);
  // Flattens all nested objects into a simple key-value format
}
```

Similarly, when generating datasets for visualization or processing, sort or transform the data at its source:

```javascript
// Instead of sorting inside the consuming component:
const generateRandomData = (days) => {
  const data = [];
  // ... generate data
  return data; // Unsorted
};

// Prefer:
const generateRandomData = (days) => {
  const data = [];
  // ... generate data
  return data.sort((a, b) => new Date(a.date) - new Date(b.date)); // Pre-sorted
};
```

This approach improves performance by avoiding redundant operations, creates cleaner separation of concerns, and makes algorithms more maintainable by handling data preparation at the appropriate level of abstraction.