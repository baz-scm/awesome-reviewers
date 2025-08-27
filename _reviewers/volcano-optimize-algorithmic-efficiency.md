---
title: Optimize algorithmic efficiency
description: Choose efficient algorithms and data structures to minimize computational
  overhead and improve code maintainability. Prefer positive logic over elimination
  methods, reuse existing data structures instead of creating new ones, and extract
  common algorithmic patterns into shared functions.
repository: volcano-sh/volcano
label: Algorithms
language: Go
comments_count: 11
repository_stars: 4899
---

Choose efficient algorithms and data structures to minimize computational overhead and improve code maintainability. Prefer positive logic over elimination methods, reuse existing data structures instead of creating new ones, and extract common algorithmic patterns into shared functions.

Key principles:
1. **Use positive validation logic**: Instead of enumerating all failure cases, validate for the expected success condition. For example, check if a node status contains only "Ready" rather than checking for "NotReady" or "Unknown".

2. **Reuse existing data structures**: Before adding new fields, evaluate if existing structures can be modified or reused. This reduces memory overhead and complexity.

3. **Extract common algorithmic patterns**: When similar logic appears in multiple places, extract it into shared functions to improve maintainability and reduce duplication.

4. **Choose efficient comparison methods**: Use built-in efficient methods like `reflect.DeepEqual()` for complex comparisons instead of manual field-by-field checks.

5. **Optimize string operations**: Use `strings.Builder` for concatenating multiple strings instead of repeated string concatenation, which has O(n²) complexity.

Example of efficient validation logic:
```go
// Inefficient: elimination method requiring enumeration
if slices.Contains(status, "NotReady") || slices.Contains(status, "Unknown") {
    return false
}

// Efficient: positive validation
if len(status) == 1 && slices.Contains(status, string(v1.NodeReady)) {
    return true
}
```

Example of efficient string building:
```go
// Inefficient: O(n²) complexity
hosts := ""
for i := 0; i < replicas; i++ {
    hosts = hosts + hostName + "." + subdomain + ","
}

// Efficient: O(n) complexity
var builder strings.Builder
for i := 0; i < replicas; i++ {
    builder.WriteString(hostName)
    builder.WriteString(".")
    builder.WriteString(subdomain)
    if i < replicas-1 {
        builder.WriteString(",")
    }
}
```