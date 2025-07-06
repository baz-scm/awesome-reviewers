---
title: Optimize performance patterns
description: 'Choose efficient implementation patterns that improve performance. Apply
  these optimizations throughout your code:


  1. **Avoid redundant operations**: Store results of expensive lookups rather than
  repeating them.'
repository: grafana/grafana
label: Performance Optimization
language: Go
comments_count: 4
repository_stars: 68825
---

Choose efficient implementation patterns that improve performance. Apply these optimizations throughout your code:

1. **Avoid redundant operations**: Store results of expensive lookups rather than repeating them.
```go
// Less efficient: searching for time field twice
for _, f := range frame.Fields {
    if f.Type() == data.FieldTypeTime {
        timeField = f
        break
    }
}
// ...later...
for _, f := range frame.Fields {
    if f.Type() == data.FieldTypeTime {
        timeField = f
        break
    }
}

// More efficient: store the reference
timeField := timeFields[frame]
```

2. **Pre-allocate when size is known**: For collections with predictable sizes, pre-allocate to avoid resizing.
```go
// Pre-allocate with known capacity
rows := make([]row, 0, totalRows)
```

3. **Properly benchmark code**: Use `b.ResetTimer()` before the actual code being benchmarked to exclude setup time.
```go
func BenchmarkOperation(b *testing.B) {
    // Setup code
    data := prepareTestData()
    
    // Start measuring only the operation we care about
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        performOperation(data)
    }
}
```

4. **Optimize database operations**: Choose the most appropriate database operation for your context. For example, after truncating a table, use regular inserts instead of upserts:
```go
// Less efficient - using upsert after truncation
if _, err := sess.Exec("DELETE FROM alert_instance"); err != nil {
    return err
}
// Then using upserts

// More efficient - using regular inserts after truncation
if _, err := sess.Exec("DELETE FROM alert_instance"); err != nil {
    return err
}
// Then using regular inserts
```

Regularly profile your code with realistic data volumes to identify and address bottlenecks.