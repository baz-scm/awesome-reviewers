---
title: Avoid unnecessary work
description: 'When optimizing performance-critical code paths, eliminate redundant
  operations and unnecessary processing:


  1. **Exit loops early** when a decision has been made and no further iterations
  are needed:'
repository: influxdata/influxdb
label: Performance Optimization
language: Go
comments_count: 4
repository_stars: 30268
---

When optimizing performance-critical code paths, eliminate redundant operations and unnecessary processing:

1. **Exit loops early** when a decision has been made and no further iterations are needed:
```go
// Good: Break out of the loop once we find what we need
for _, f := range files {
    if tsmPointsPerBlock := fileStore.BlockCount(f, 1); tsmPointsPerBlock == aggressivePointsPerBlock {
        pointsPerBlock = aggressivePointsPerBlock
        break // No need to check remaining files
    }
}
```

2. **Cache calculated values** that are used multiple times, especially expensive calculations:
```go
// Good: Calculate time bounds once and reuse
futureTimeLimit := time.Now().Add(rp.FutureWriteLimit)
pastTimeLimit := time.Now().Add(-rp.PastWriteLimit)

// Check points against cached limits
for _, p := range points {
    if p.Time().After(futureTimeLimit) || p.Time().Before(pastTimeLimit) {
        // Point outside time window
    }
}
```

3. **Skip reprocessing** data that already meets target criteria:
```go
// Good: Use >= instead of == to avoid recompacting already optimized files
if blockCount >= targetBlockCount && !hasTombstones {
    // Skip this file, it's already optimized
}
```

4. **Use direct operations** rather than unnecessary function calls for deterministic results:
```go
// Good: Use copy directly instead of looping with a function that always returns true
shards := make([]*Shard, 0, len(s.shards))
copy(shards, s.shards)
```

These optimizations reduce CPU cycles, memory allocations, and I/O operations, leading to more efficient code execution, particularly in performance-sensitive areas.