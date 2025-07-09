---
title: Optimize memory allocation
description: Always allocate data structures with appropriate initial capacity and
  use memory-efficient data types to reduce memory pressure and improve application
  performance. Pre-allocate containers when the size is known or can be estimated,
  avoid unnecessary intermediate data structures, and choose compact data representations.
repository: vitessio/vitess
label: Performance Optimization
language: Go
comments_count: 5
repository_stars: 19815
---

Always allocate data structures with appropriate initial capacity and use memory-efficient data types to reduce memory pressure and improve application performance. Pre-allocate containers when the size is known or can be estimated, avoid unnecessary intermediate data structures, and choose compact data representations.

For example:

```go
// Good: Pre-allocate with known capacity
finalRes := make(map[string]string, len(qr.Rows))
errors := make(map[string][]error, 1)  // When expecting few entries

// Good: Use memory-efficient data types
// TabletAlias object (8 bytes) vs string representation (16 bytes)
type queueItem struct {
    TabletAlias *topodatapb.TabletAlias  // More memory-efficient
    // Instead of: Key string  // Less efficient
}

// Good: Avoid unnecessary intermediate data structures
// Direct processing without creating intermediate collections
var offset int64
var fieldsIndex int
for i, loc := range bindLocations {
    field = tp.Fields[fieldsIndex]
    length = row.Lengths[fieldsIndex]
    // Process directly...
}
```

Memory allocation patterns have significant impact on both CPU and memory performance, especially in high-throughput services. Inefficient allocations create unnecessary garbage collection pressure, leading to more frequent GC cycles and higher CPU usage. By being thoughtful about memory allocation, you can achieve substantial performance improvements with minimal code changes.