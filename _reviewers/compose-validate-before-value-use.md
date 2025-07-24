---
title: Validate before value use
description: Always validate potentially null or empty values before use, and provide
  explicit default values when handling optional data. This prevents runtime errors
  and makes code behavior more predictable.
repository: docker/compose
label: Null Handling
language: Go
comments_count: 3
repository_stars: 35858
---

Always validate potentially null or empty values before use, and provide explicit default values when handling optional data. This prevents runtime errors and makes code behavior more predictable.

Key practices:
1. Check for empty strings before processing
2. Provide type-safe default values for optional data
3. Use explicit nil checks for optional references

Example:
```go
// Before
func processValue(m map[string]interface{}, key string) string {
    return m[key].(string)
}

// After
func processValue(m map[string]interface{}, key string) string {
    if v, ok := m[key].(string); ok && v != "" {
        return v
    }
    return "" // explicit default
}

// Even better with generics
func valueOrDefault[T any](m map[string]interface{}, key string) T {
    if v, ok := m[key].(T); ok {
        return v
    }
    return *new(T)
}
```