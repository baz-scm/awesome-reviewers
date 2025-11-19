---
title: minimize resource usage
description: Optimize performance by being selective about resource consumption -
  process only necessary data, avoid redundant operations, and use lightweight alternatives
  when possible.
repository: nrwl/nx
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 27518
---

Optimize performance by being selective about resource consumption - process only necessary data, avoid redundant operations, and use lightweight alternatives when possible.

Key strategies:
- **Store hashes instead of full data**: Rather than caching entire objects, store their hashes to reduce disk space and computation overhead
- **Reduce data before processing**: Filter or transform data to minimal required form before expensive operations like hashing
- **Avoid redundant operations**: Ensure expensive operations like hashing are performed only once and reused
- **Use conditional loading**: Only require/import modules when actually needed, and prefer `require.resolve()` over `require()` when you don't need to execute the module

Example:
```javascript
// Instead of storing full external nodes data
const externalNodesData = getExternalNodesData(externalNodes);
writeToCache(externalNodesData); // Large disk usage

// Store hash instead
const externalNodesHash = hashObject(getExternalNodesData(externalNodes));
writeToCache(externalNodesHash); // Minimal disk usage

// Conditional require
function assertBuilderPackageIsInstalled(packageName: string): void {
  try {
    require.resolve(packageName); // Lighter than require(packageName)
  } catch {
    throw new Error(`Package ${packageName} not found`);
  }
}
```

This approach can yield significant performance improvements - benchmarks show up to 6x speed improvements when reducing data before processing.