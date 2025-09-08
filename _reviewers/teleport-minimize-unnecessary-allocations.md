---
title: minimize unnecessary allocations
description: 'Avoid unnecessary memory allocations in performance-critical code paths,
  especially in frequently executed functions or loops that process large datasets.
  Common allocation sources to eliminate include:'
repository: gravitational/teleport
label: Performance Optimization
language: Go
comments_count: 5
repository_stars: 19109
---

Avoid unnecessary memory allocations in performance-critical code paths, especially in frequently executed functions or loops that process large datasets. Common allocation sources to eliminate include:

1. **Intermediate collections**: Iterate directly over data structures instead of creating temporary slices or maps
2. **Buffer reuse**: Reuse existing buffers or pass io.Writer interfaces to avoid extra copies
3. **Map/slice reuse**: Swap and clear existing collections instead of allocating new ones
4. **String operations**: Use direct string concatenation or efficient formatting instead of fmt.Sprintf in hot paths
5. **Preallocation**: Only preallocate collections when you know they will be populated in the common case

Example of eliminating intermediate slice:
```go
// Before: Creates unnecessary intermediate slice
proxyAddrs := make([]string, 0, len(proxyServers))
for _, proxyServer := range proxyServers {
    proxyAddrs = append(proxyAddrs, proxyServer.GetPublicAddr())
}
for _, proxyAddr := range proxyAddrs {
    // process proxyAddr
}

// After: Direct iteration
for _, proxyServer := range proxyServers {
    proxyAddr := proxyServer.GetPublicAddr()
    // process proxyAddr directly
}
```

Example of avoiding fmt.Sprintf in index functions:
```go
// Before: Expensive formatting in frequently called function
return fmt.Sprintf("%s/%s", date.Format(time.RFC3339), name)

// After: Direct string concatenation
return date.Format("20060102") + "/" + name
```

This optimization is particularly important for functions called frequently, index operations on large collections, or code paths processing thousands of items.