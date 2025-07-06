---
title: Type over primitives
description: 'Use domain-specific types instead of primitives (like strings, []byte,
  or generic maps) to represent domain concepts in algorithms. This makes assumptions
  explicit, prevents errors, and enables stronger type checking. For example, rather
  than passing raw byte slices for different kinds of series keys:'
repository: influxdata/influxdb
label: Algorithms
language: Go
comments_count: 3
repository_stars: 30268
---

Use domain-specific types instead of primitives (like strings, []byte, or generic maps) to represent domain concepts in algorithms. This makes assumptions explicit, prevents errors, and enables stronger type checking. For example, rather than passing raw byte slices for different kinds of series keys:

```go
// Problematic approach - using raw []byte
func parseSeriesKey(key []byte) (measurement, tags []byte) {
    // Code assumes specific format without enforcing it
    // Easy to pass wrong key format!
}

// Better approach - using typed wrapper
type SeriesKeyV1 struct {
    B []byte
}

type SeriesKeyV2 struct {
    B []byte
}

func parseSeriesKeyV1(key SeriesKeyV1) (measurement, tags []byte) {
    // Implementation specific to V1 format
}

func parseSeriesKeyV2(key SeriesKeyV2) (measurement, tags []byte) {
    // Implementation specific to V2 format
}
```

This pattern applies to many algorithms like filtering functions, composite predicates, and data transformations. By creating specific types, you prevent algorithmic errors, make code more readable, and ensure operations only apply to valid inputs. Type-safe algorithms are easier to reason about and less prone to subtle bugs.