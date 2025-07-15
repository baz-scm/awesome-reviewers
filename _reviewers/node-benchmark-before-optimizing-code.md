---
title: Benchmark before optimizing code
description: Performance optimizations should be validated through benchmarks before
  implementation. This helps prevent premature optimization and ensures changes actually
  improve performance in real-world scenarios.
repository: nodejs/node
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 112178
---

Performance optimizations should be validated through benchmarks before implementation. This helps prevent premature optimization and ensures changes actually improve performance in real-world scenarios.

Key practices:
1. Run benchmarks to establish baseline performance
2. Test multiple input sizes to find stabilization points
3. Consider edge cases and different environments
4. Document benchmark results in the PR

Example:
```javascript
// Before optimizing this:
const pairs = ArrayPrototypeMap(entries, ({ 0: k, 1: v }) => `${k}:${v}`);

// Run benchmarks to validate if this is better:
let pairs = new Array(entries.length);
for (let i = 0; i < entries.length; i++) {
  pairs[i] = `${entries[i][0]}:${entries[i][1]}`;
}

/* Example benchmark results:
n=10:        19,123 ops/sec
n=100:      222,985 ops/sec
n=1000:   1,262,360 ops/sec
n=10000:  3,751,348 ops/sec
n=100000: 4,789,673 ops/sec
*/
```

This approach helps prevent optimization work that doesn't provide meaningful benefits while identifying changes that do improve performance significantly.