---
title: benchmark performance assumptions
description: Always validate performance assumptions with concrete benchmarks rather
  than making optimization decisions based on intuition. When considering performance
  trade-offs between different implementation approaches, write targeted benchmarks
  to measure the actual impact.
repository: denoland/deno
label: Performance Optimization
language: JavaScript
comments_count: 2
repository_stars: 103714
---

Always validate performance assumptions with concrete benchmarks rather than making optimization decisions based on intuition. When considering performance trade-offs between different implementation approaches, write targeted benchmarks to measure the actual impact.

For example, when debating between using arrays vs multiple function arguments, benchmark both approaches:

```javascript
// Don't assume - measure the difference
// Option 1: Array approach
return respond(id, [{}, null]);

// Option 2: Multiple arguments  
return respond(id, {}, null);
```

The benchmark revealed that "adding another arg is about 15% slower than the array version", leading to a data-driven decision to keep the array approach.

Similarly, when choosing between async and sync operations, measure the performance impact in your specific context rather than following general patterns. What works for browsers may not be optimal for your runtime environment.

This approach prevents premature optimization, ensures changes actually improve performance, and helps avoid performance regressions disguised as improvements.