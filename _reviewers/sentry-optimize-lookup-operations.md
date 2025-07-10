---
title: Optimize lookup operations
description: Choose appropriate data structures to minimize computational complexity
  when performing lookups. Prefer direct lookups (maps/dictionaries) over repeated
  array traversals, and use set-based inclusion checks for membership testing rather
  than multiple conditionals.
repository: getsentry/sentry
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 41297
---

Choose appropriate data structures to minimize computational complexity when performing lookups. Prefer direct lookups (maps/dictionaries) over repeated array traversals, and use set-based inclusion checks for membership testing rather than multiple conditionals.

**Instead of repeatedly traversing arrays:**
```typescript
// Inefficient - requires O(n) lookup each time
const integration = props.integrations.find(({key}) => key === value);
if (!integration) {
  return true;
}
```

**Consider:**
1. Creating lookup maps for frequently accessed collections
```typescript
// O(1) lookup after initial map creation
const integrationsByKey = new Map(props.integrations.map(i => [i.key, i]));
const integration = integrationsByKey.get(value);
```

2. Using array inclusion for multiple condition checks
```typescript
// Instead of multiple OR conditions:
// if (aggregation === AggregationKey.EPM || aggregation === AggregationKey.EPS) {

// More maintainable and extensible approach:
if (aggregation && NO_ARGUMENT_SPAN_AGGREGATES.includes(aggregation as AggregationKey)) {
```

This approach not only improves performance for large datasets but also makes code more maintainable when conditions need to be added or removed in the future.