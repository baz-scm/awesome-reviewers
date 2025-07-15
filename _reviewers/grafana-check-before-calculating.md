---
title: Check before calculating
description: Implement preliminary validation checks before executing expensive operations
  to avoid unnecessary processing. When handling operations that may be computationally
  intensive (like text layout calculations, data transformations, or complex rendering),
  add targeted checks that can early-exit or skip work when the operation would have
  no effect or be redundant.
repository: grafana/grafana
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 68825
---

Implement preliminary validation checks before executing expensive operations to avoid unnecessary processing. When handling operations that may be computationally intensive (like text layout calculations, data transformations, or complex rendering), add targeted checks that can early-exit or skip work when the operation would have no effect or be redundant.

For example, when calculating text wrapping dimensions:

```typescript
// Before optimization
const calcRowHeight = (text: string, cellWidth: number, defaultHeight: number) => {
  const numLines = count(text, cellWidth);
  const totalHeight = numLines * TABLE.LINE_HEIGHT + 2 * TABLE.CELL_PADDING;
  return Math.max(totalHeight, defaultHeight);
};

// After optimization
const calcRowHeight = (text: string, cellWidth: number, defaultHeight: number) => {
  // Skip expensive line counting if text has no spaces (can't wrap)
  if (!text || !/[\s]+/.test(text)) {
    return defaultHeight;
  }
  
  const numLines = count(text, cellWidth);
  const totalHeight = numLines * TABLE.LINE_HEIGHT + 2 * TABLE.CELL_PADDING;
  return Math.max(totalHeight, defaultHeight);
};
```

Always validate optimization checks with performance profiling on representative data sets to ensure they actually improve performance and don't introduce regressions.