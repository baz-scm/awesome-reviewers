---
title: Avoid expensive repeated operations
description: Identify and eliminate expensive operations that are performed repeatedly,
  such as object creation in loops, redundant computations, or duplicate filtering
  operations. Cache expensive objects like RegExp instances, i18n instances, or computed
  results to improve performance and prevent memory leaks.
repository: twentyhq/twenty
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 35477
---

Identify and eliminate expensive operations that are performed repeatedly, such as object creation in loops, redundant computations, or duplicate filtering operations. Cache expensive objects like RegExp instances, i18n instances, or computed results to improve performance and prevent memory leaks.

Examples of optimization:
- Cache RegExp objects outside loops instead of creating them repeatedly
- Use instance maps to reuse expensive objects like i18n instances
- Store intermediate results when filtering or processing the same data multiple times
- Optimize data structure initialization (e.g., use `new Map(array.map())` instead of forEach loops)

```javascript
// Bad: Creating RegExp in loop
for (const [accented, unaccented] of Object.entries(specialChars)) {
  result = result.replace(new RegExp(accented, 'g'), unaccented);
}

// Good: Single RegExp with callback
const specialCharsRegex = new RegExp(`[${Object.keys(specialChars).join('')}]`, 'g');
return text.replace(specialCharsRegex, (match) => specialChars[match]);

// Bad: Filtering same array twice
const filtered1 = enrichedSeries.filter(series => series.shouldEnableArea);
const filtered2 = enrichedSeries.filter(series => series.shouldEnableArea);

// Good: Store intermediate result
const areaEnabledSeries = enrichedSeries.filter(series => series.shouldEnableArea);
```