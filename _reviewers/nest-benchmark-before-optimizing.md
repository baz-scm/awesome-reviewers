---
title: Benchmark before optimizing
description: When making performance-critical decisions, always validate your approach
  with benchmarks using realistic data sizes and use cases rather than relying on
  theoretical assumptions.
repository: nestjs/nest
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 71766
---

When making performance-critical decisions, always validate your approach with benchmarks using realistic data sizes and use cases rather than relying on theoretical assumptions.

For data access patterns, benchmark different approaches with varying data sizes:

```javascript
// Example benchmark comparing Array, Map and Object lookups
function runBenchmark(dataSize, iterations) {
  const data = generateTestData(dataSize);
  const structures = prepareDataStructures(data);

  const structureTypes = ['array', 'map', 'object'];
  const results = {};
  const queryKeys = Array.from({ length: iterations }, () =>
    structures.arr[Math.floor(Math.random() * dataSize)].key
  );

  structureTypes.forEach(structure => {
    const start = performance.now();
    queryKeys.forEach(key => runQuery(structure, key, structures));
    const end = performance.now();
    results[structure] = end - start;
  });

  console.log(`Data size: ${dataSize}, Iterations: ${iterations}`);
  structureTypes.forEach(structure => {
    console.log(`${structure}: ${results[structure]}ms`);
  });
}
```

When optimizing loops or operations on collections, compare functional approaches (map/filter) against traditional loops with measurements rather than intuition:

```javascript
// Quick performance comparison
function benchmarkApproaches() {
  console.time('functional');
  const result1 = array.map(process).filter(isValid);
  console.timeEnd('functional');
  
  console.time('for-loop');
  const result2 = [];
  for (const item of array) {
    const processed = process(item);
    if (isValid(processed)) {
      result2.push(processed);
    }
  }
  console.timeEnd('for-loop');
}
```

Consider early termination when applicable (finding first match vs processing all elements), and test with various data sizes that represent your actual workload. Balancing readability with performance is essential - only sacrifice readability when benchmarks demonstrate a significant performance advantage in performance-critical paths.