---
title: Explicit null validation
description: Always validate objects for null/nil before accessing their properties,
  and establish consistent patterns for handling null values throughout the codebase.
  This prevents nil pointer dereferences and ensures predictable behavior.
repository: grafana/grafana
label: Null Handling
language: Go
comments_count: 6
repository_stars: 68825
---

Always validate objects for null/nil before accessing their properties, and establish consistent patterns for handling null values throughout the codebase. This prevents nil pointer dereferences and ensures predictable behavior.

Three key practices:

1. **Add explicit null checks before property access:**
```go
// Bad: May cause nil pointer dereference
accessorReturned, err := meta.Accessor(returnedObj)

// Good: Check for nil first
if returnedObj == nil {
    return nil, errors.New("cannot enrich nil object")
}
accessorReturned, err := meta.Accessor(returnedObj)
```

2. **Use proper objects instead of nil values:**
```go
// Bad: Using nil objects that may cause dereference errors
return newRecordingRule(context.Background(), models.AlertRuleKeyWithGroup{}, 0, nil, nil, st, log.NewNopLogger(), nil, nil, writer.FakeWriter{}, nil, nil)

// Good: Use proper initialized objects
mockClock := clock.NewMock()
retryConfig := RetryConfig{
    MaxRetries:    3,
    RetryInterval: time.Second,
}
return newRecordingRule(context.Background(), models.AlertRuleKeyWithGroup{}, retryConfig, mockClock, nil, st, log.NewNopLogger(), nil, nil, writer.FakeWriter{}, nil, nil)
```

3. **Document and implement consistent null handling behavior:**
   - Clearly define when functions should return nil vs. empty objects vs. default values
   - Ensure consistent implementation across the codebase
   - Check if objects are nil before performing operations on them, especially in migrations and data processing

When handling special cases like empty strings or missing values, document the expected behavior and ensure all developers follow the same patterns.