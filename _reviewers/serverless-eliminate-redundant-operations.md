---
title: Eliminate redundant operations
description: Identify and eliminate repeated expensive operations to improve performance.
  Look for opportunities to cache results, avoid duplicate computations, and minimize
  unnecessary work.
repository: serverless/serverless
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 46810
---

Identify and eliminate repeated expensive operations to improve performance. Look for opportunities to cache results, avoid duplicate computations, and minimize unnecessary work.

Key strategies:
- **Memoize expensive operations**: Cache results of file reads, hash computations, and API responses that are called multiple times
- **Avoid redundant parsing**: Don't parse the same data multiple times; use simple checks like `item.startsWith('[')` before expensive operations like `JSON.parse()`
- **Skip unnecessary operations**: Check if work is actually needed before performing it (e.g., check if ECR repository exists before attempting removal)
- **Use efficient file operations**: Prefer moving files over copying when working with temporary directories

Example of memoization:
```javascript
// Before: Reading package.json multiple times
const packageJson = JSON.parse(fs.readFileSync('package.json'));

// After: Memoize the operation
this._readPackageJson = _.memoize(this._readPackageJson.bind(this));
```

Example of avoiding redundant parsing:
```javascript
// Before: JSON.parse in both filter and map
.filter((item) => item !== '' && Array.isArray(JSON.parse(item)))
.map((item) => JSON.parse(item))

// After: Simple check first, parse once
.filter((item) => item.startsWith('['))
.map((item) => JSON.parse(item))
```

This approach reduces CPU usage, memory allocation, and I/O operations, leading to faster execution times and better resource utilization.