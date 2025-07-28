---
title: Measure performance impacts
description: Always benchmark and measure actual performance impacts before making
  optimization decisions, rather than relying on assumptions. Performance characteristics
  can vary significantly across different runtimes, data sizes, and usage patterns.
repository: prettier/prettier
label: Performance Optimization
language: JavaScript
comments_count: 4
repository_stars: 50772
---

Always benchmark and measure actual performance impacts before making optimization decisions, rather than relying on assumptions. Performance characteristics can vary significantly across different runtimes, data sizes, and usage patterns.

When optimizing code:
- Conduct micro-benchmarks for critical paths to compare alternatives
- Consider runtime-specific performance characteristics (e.g., "Array#at is slow on Node.js v16 and v18")
- Measure real-world performance improvements and adjust expectations accordingly
- Balance trade-offs between code clarity and performance based on actual data

Example from codebase:
```javascript
// Micro benchmarking showed trim().length was faster than regex
// Choose based on measurement, not assumption
const keepTypeCast = text.slice(locEnd(previousComment), locStart(node)).trim().length === 0;
// vs
const keepTypeCast = !/\S/.test(text.slice(locEnd(previousComment), locStart(node)));
```

For performance-critical code, document the reasoning behind optimization choices and include performance test cases that can detect regressions. When performance improves significantly (e.g., 10x faster), update test expectations to catch future performance degradations.