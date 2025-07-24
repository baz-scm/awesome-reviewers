---
title: avoid panics gracefully
description: Never use panic() for error handling in production code paths, especially
  in core engine components. Instead, handle errors gracefully by returning appropriate
  values or ignoring problematic data with optional warnings.
repository: prometheus/prometheus
label: Error Handling
language: Go
comments_count: 5
repository_stars: 59616
---

Never use panic() for error handling in production code paths, especially in core engine components. Instead, handle errors gracefully by returning appropriate values or ignoring problematic data with optional warnings.

When encountering errors during operations like histogram arithmetic or data processing, prefer these approaches:
- Return a "keep=false" flag to indicate the value should be discarded
- Return nil/zero values to skip the problematic operation  
- Log warnings for debugging while continuing execution
- Use error annotations for user-facing feedback instead of crashing

Example of problematic code:
```go
res, err := hlhs.Copy().Add(hrhs)
if err != nil {
    panic(err) // DON'T DO THIS
}
```

Better approach:
```go
res, err := hlhs.Copy().Add(hrhs)
if err != nil {
    return 0, nil, false // Gracefully indicate failure
}
```

This ensures system stability and prevents cascading failures from individual data processing errors. Panics should only be reserved for truly unrecoverable programming errors during development, not for handling expected error conditions in production.