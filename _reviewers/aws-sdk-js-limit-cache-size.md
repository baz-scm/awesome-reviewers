---
title: Limit cache size
description: Always implement size constraints on caches to prevent memory leaks and
  performance degradation. Unbounded caches can grow continuously and consume excessive
  memory, especially in long-running applications.
repository: aws/aws-sdk-js
label: Caching
language: JavaScript
comments_count: 3
repository_stars: 7628
---

Always implement size constraints on caches to prevent memory leaks and performance degradation. Unbounded caches can grow continuously and consume excessive memory, especially in long-running applications.

Key implementation practices:
1. Set a maximum entry count for each cache
2. Implement an eviction strategy (like LRU - Least Recently Used)
3. Design efficient cache keys that include only necessary information
4. Consider providing cache control options to users

Example implementation of a size-constrained cache:

```javascript
// Cache with maximum size limit and LRU eviction
var cachedSecret = {};
var cacheQueue = [];
var maxCacheEntries = 50;

function addToCache(key, value) {
  // If cache is full, remove oldest entry
  if (cacheQueue.length >= maxCacheEntries) {
    var oldestKey = cacheQueue.shift();
    delete cachedSecret[oldestKey];
  }
  
  // Add new entry
  cachedSecret[key] = value;
  cacheQueue.push(key);
}

// Generate minimal but sufficient cache keys
function getCacheKey(request) {
  // Only include required identifiers to keep cache size manageable
  var identifiers = {};
  // Add essential properties for uniqueness
  // Omit unnecessary data to minimize cache size
  return identifiers;
}
```

This approach prevents memory issues in applications that might generate many cache entries over time, while maintaining the performance benefits of caching.
