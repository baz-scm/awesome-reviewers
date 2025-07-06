---
title: Measure before optimizing
description: 'Performance optimizations should be validated with measurements rather
  than assumptions. When implementing performance-sensitive code or optimizations:'
repository: grafana/grafana
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 68825
---

Performance optimizations should be validated with measurements rather than assumptions. When implementing performance-sensitive code or optimizations:

1. Measure the performance impact with realistic data volumes (small, medium, and large scale)
2. Document the performance metrics in comments to justify decisions
3. Consider the tradeoffs between implementation complexity and actual performance gains
4. Clean up resources explicitly to prevent memory leaks

**Example:**
```typescript
// Performance tested with:
// - 100k points: ~180ms initialization overhead
// - 10k points: ~20ms initialization overhead
// - 1k points: ~2ms initialization overhead
// Optimization is worthwhile for common use cases with >1k points

// Track coordinates to avoid rendering duplicate markers
const processedCoordinates = new Set<string>();

// Clean up resources when component unmounts
useEffect(() => {
  return () => {
    if (imageBlob) {
      URL.revokeObjectURL(URL.createObjectURL(imageBlob));
    }
  };
}, [imageBlob]);
```

This approach ensures optimization efforts are focused on areas with measurable impact and helps prevent premature optimization that could introduce unnecessary complexity.