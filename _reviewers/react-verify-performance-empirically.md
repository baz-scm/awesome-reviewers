---
title: "Verify performance empirically"
description: "Always validate performance optimizations through measurement rather than assumptions. Run multiple iterations of performance tests to ensure statistical significance and reduce noise in your metrics."
repository: "facebook/react"
label: "Performance Optimization"
language: "TypeScript"
comments_count: 3
repository_stars: 237000
---

Always validate performance optimizations through measurement rather than assumptions. Run multiple iterations of performance tests to ensure statistical significance and reduce noise in your metrics.

When proposing performance-related changes:
1. Establish baseline measurements before making changes
2. Implement your optimization
3. Run the same tests multiple times (at least 5 iterations)
4. Calculate average metrics to verify actual improvement

```javascript
// Example: Multiple iterations for reliable performance testing
const iterations = 5;
let totalRenderTime = 0;

// Collect performance data across multiple runs
for (let i = 0; i < iterations; i++) {
  const performance = await measurePerformance(component);
  totalRenderTime += performance.renderTime;
}

// Calculate and report the average
const averageRenderTime = totalRenderTime / iterations;
console.log(`Average render time: ${averageRenderTime.toFixed(2)}ms`);
```

This approach prevents changes that might appear beneficial in a single test run but actually have neutral or negative impacts in production environments. Increasing the number of iterations provides higher confidence in your performance results.