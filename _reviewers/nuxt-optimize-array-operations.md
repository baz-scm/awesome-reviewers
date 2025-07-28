---
title: optimize array operations
description: Pre-allocate arrays when the final size is known and consolidate multiple
  iterations into single loops to reduce memory allocations and improve performance.
repository: nuxt/nuxt
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 57769
---

Pre-allocate arrays when the final size is known and consolidate multiple iterations into single loops to reduce memory allocations and improve performance.

When you know the array size in advance, use `new Array(length)` instead of starting with an empty array and using `push()`. JavaScript engines allocate extra space (typically 8-16 slots) when using `push()`, leading to wasted memory.

Combine multiple array operations (map, filter, forEach) into a single loop when possible to reduce iterations and temporary array creation.

**Example - Array pre-allocation:**
```javascript
// Instead of this:
const vnodes = []
for (const item of items) {
  vnodes.push(processItem(item))
}

// Do this when size is known:
const vnodes = new Array(items.length)
for (let i = 0; i < items.length; i++) {
  vnodes[i] = processItem(items[i])
}
```

**Example - Consolidating iterations:**
```javascript
// Instead of multiple operations:
const filtered = items.filter(item => item.enabled)
const mapped = filtered.map(item => transform(item))
const processed = mapped.forEach(item => process(item))

// Use single loop:
const results = []
for (const item of items) {
  if (item.enabled) {
    const transformed = transform(item)
    results.push(transformed)
    process(transformed)
  }
}
```

This approach reduces both memory allocations and CPU cycles, especially beneficial when processing large datasets or in performance-critical code paths.