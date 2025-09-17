---
title: optimize data structure lookups
description: Choose data structures that provide optimal time complexity for your
  access patterns. When you need frequent lookups by key, use Map instead of Record
  with Array.find() operations to achieve O(1) instead of O(n) complexity.
repository: twentyhq/twenty
label: Algorithms
language: TypeScript
comments_count: 2
repository_stars: 35477
---

Choose data structures that provide optimal time complexity for your access patterns. When you need frequent lookups by key, use Map instead of Record with Array.find() operations to achieve O(1) instead of O(n) complexity.

The most common anti-pattern is building a Record and then using Array.find() to search through collections, which results in O(n) time complexity for each lookup. Instead, use Map for constant-time lookups.

Example of inefficient approach:
```typescript
const dataMap: Record<string, LineChartSeries> = {};
for (const series of data) {
  dataMap[series.id] = series;
}

// Later, expensive O(n) lookup:
const enrichedSeriesItem = enrichedSeries.find(
  (item) => item.id === someId
);
```

Optimized approach:
```typescript
const dataMap = new Map<string, LineChartSeries>(
  data.map((series) => [series.id, series])
);

// Later, efficient O(1) lookup:
const enrichedSeriesItem = dataMap.get(someId);
```

This optimization is particularly important in frequently called functions, loops, or when dealing with large datasets where the performance difference becomes significant.