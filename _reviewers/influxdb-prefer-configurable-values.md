---
title: Prefer configurable values
description: Always use configurable values instead of hardcoded defaults when available.
  This ensures that user preferences are respected throughout the application lifecycle
  and prevents unexpected behavior.
repository: influxdata/influxdb
label: Configurations
language: Go
comments_count: 4
repository_stars: 30268
---

Always use configurable values instead of hardcoded defaults when available. This ensures that user preferences are respected throughout the application lifecycle and prevents unexpected behavior.

When defining related configuration constants, establish their relationship explicitly rather than using magic numbers:

```go
// Bad
const DefaultMaxPointsPerBlock = 1000
const AggressiveMaxPointsPerBlock = 100000  // Magic number with unclear relationship

// Good
const DefaultMaxPointsPerBlock = 1000
const AggressiveMaxPointsPerBlock = DefaultMaxPointsPerBlock * 100  // Relationship is clear and maintainable
```

When referencing configuration values in logs or error messages, clearly indicate whether you're using a default or a user-configured value:

```go
// Bad
e.logger.Info("TSM optimized compaction running", 
    zap.Int("points-per-block", tsdb.DefaultAggressiveMaxPointsPerBlock))

// Good
e.logger.Info("TSM optimized compaction running", 
    zap.Int("points-per-block", e.CompactionPlan.GetAggressiveCompactionPointsPerBlock()))

// Good - when referencing defaults in messages
fmt.Sprintf("points per block count (default: %d points)", DefaultAggressiveMaxPointsPerBlock)
```

Always check against configured values rather than defaults when making decisions in your code. This respects user settings and prevents unexpected behavior when configurations change.