---
title: Context-aware network calls
description: Always propagate context through network calls to ensure proper cancellation,
  timeout handling, and tracing. For HTTP requests, use `http.NewRequestWithContext()`
  instead of `http.Post()` or `http.Get()`. For gRPC, ensure context is passed and
  enriched with necessary metadata.
repository: temporalio/temporal
label: Networking
language: Go
comments_count: 3
repository_stars: 14953
---

Always propagate context through network calls to ensure proper cancellation, timeout handling, and tracing. For HTTP requests, use `http.NewRequestWithContext()` instead of `http.Post()` or `http.Get()`. For gRPC, ensure context is passed and enriched with necessary metadata.

When adding metadata to context:
- For single values, use `metadata.AppendToOutgoingContext(ctx, key, value)`
- For multiple values, batch them in a single call: `metadata.AppendToOutgoingContext(ctx, k1, v1, k2, v2, ...)`

Example of context-aware HTTP client:
```go
// Instead of this:
response, err := http.Post(a.opaEndpoint, "application/json", bytes.NewBuffer(jsonData))

// Do this:
req, err := http.NewRequestWithContext(ctx, "POST", a.opaEndpoint, bytes.NewBuffer(jsonData))
if err != nil {
    return resultDeny, err
}
req.Header.Set("Content-Type", "application/json")
response, err := http.DefaultClient.Do(req)
```

Example of proper gRPC context metadata:
```go
// Batch metadata in a single call
ctx = metadata.AppendToOutgoingContext(ctx, 
    "temporal-test-name", testName,
    "user-id", userId,
    "request-id", requestId)
```

Context propagation ensures that cancellation signals are properly passed throughout the system, preventing resource leaks and allowing proper tracing of distributed operations.