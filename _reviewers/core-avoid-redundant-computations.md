---
title: Avoid redundant computations
description: Identify and eliminate redundant operations that cause performance bottlenecks
  by caching expensive function results, performing transformations only when necessary,
  and implementing lazy evaluation patterns.
repository: vuejs/core
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 50769
---

Identify and eliminate redundant operations that cause performance bottlenecks by caching expensive function results, performing transformations only when necessary, and implementing lazy evaluation patterns.

Key optimization strategies:

1. Cache expensive function results that may be reused:
```javascript
// Before - recalculates camelize(key) multiple times
if (camelize(key) in el || key in el) {
  // do something
}

// After - calculates once and reuses
const camelKey = camelize(key)
if (camelKey in el || key in el) {
  // do something
}
```

2. Apply transformations selectively rather than to all elements:
```javascript
// Before - unnecessarily transforms all arguments
return arr[key](...args.map(toRaw))

// After - transforms only what's needed
return arr[key](toRaw(args[0]), ...args.slice(1))
```

3. Use lazy evaluation for expensive operations:
```javascript
// Before - calculates expensive operation eagerly
if (dep.get(effect) === effect._trackId && effect._runnings > 0) {
  // use result
}

// After - calculates only when needed
let tracking: boolean | undefined
if ((tracking ??= dep.get(effect) === effect._trackId) && effect._runnings > 0) {
  // use tracking value
}
```

4. Initialize data structures with values directly when possible:
```javascript
// Before - less efficient
const queue = []
queue.push(['a', 1])

// After - more efficient (benchmark: ~2.25x faster)
const queue = [['a', 1]]
```

5. Pass appropriate flags to avoid unnecessary work:
```javascript
// Before
for (let child = this.scopes; child != undefined; child = child.nextEffectScope) {
  child.stop();
}

// After - avoids unnecessary unlinking operations
for (let child = this.scopes; child != undefined; child = child.nextEffectScope) {
  child.stop(true)
}
```

These optimizations become particularly important in hot paths that execute frequently or when working with large data structures.