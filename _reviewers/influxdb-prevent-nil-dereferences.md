---
title: Prevent nil dereferences
description: Always verify that pointers, slices, or arrays are non-nil and have sufficient
  elements before attempting to access their members. Use appropriate checks in the
  correct order to prevent runtime panics.
repository: influxdata/influxdb
label: Null Handling
language: Go
comments_count: 4
repository_stars: 30268
---

Always verify that pointers, slices, or arrays are non-nil and have sufficient elements before attempting to access their members. Use appropriate checks in the correct order to prevent runtime panics.

For pointers:
```go
// Do this
if a != nil {
    a.Token = "value"  // Safe access
}

// Not this
a.Token = "value"  // Potential panic if a is nil
```

For arrays and slices:
```go
// Do this - check length before indexing
if len(gens) > 0 {
    size := gens[0].size()  // Safe access
}

// Not this
size := gens[0].size()  // Potential panic if gens is empty
```

When checking for nil slices, remember that `len()` already handles nil slices correctly (returning 0), so separate nil checks are often redundant:

```go
// This is sufficient
if len(fns) == 0 {
    // handle empty case
}

// Not this - redundant check
if fns == nil || len(fns) == 0 {
    // handle empty case
}
```

However, if you do need both checks for clarity or other reasons, always check for nil first:

```go
// Do this - nil check first to avoid potential panic
if fns == nil || someOtherCondition(fns) {
    // handle nil case
}
```

This practice helps prevent common runtime errors like nil pointer dereferences and index out of range panics.