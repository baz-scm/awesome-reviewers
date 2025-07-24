---
title: simplify test structure
description: Write tests that are direct, focused, and free of unnecessary complexity.
  Remove redundant test fields, use direct assertions with expected values, and leverage
  existing fixtures instead of creating temporary content.
repository: prometheus/prometheus
label: Testing
language: Go
comments_count: 5
repository_stars: 59616
---

Write tests that are direct, focused, and free of unnecessary complexity. Remove redundant test fields, use direct assertions with expected values, and leverage existing fixtures instead of creating temporary content.

**Key principles:**
- Remove unnecessary test case fields that aren't actually used in assertions
- Use direct comparisons (`require.Equal`) with expected output instead of calculating or checking properties within tests
- Leverage existing fixture files and glob patterns rather than creating temporary files and content
- Keep tests focused on a single responsibility - split tests that cover multiple features
- Use appropriate abstraction levels (prefer higher-level integration tests over low-level unit tests that re-implement logic)

**Example of simplification:**
```go
// Before: Complex test with unused fields
type test struct {
    errType errorType
    err     error          // unused
    resCode int
    msg     string         // unused
    errTypeToStatusCode ErrorTypeToStatusCode
}

// After: Simplified test structure
type test struct {
    errType             errorType
    resCode             int
    errTypeToStatusCode ErrorTypeToStatusCode
}

// Use direct values instead of variables
api.respondError(w, &apiError{tc.errType, errors.New("message")}, "test")
```

This approach makes tests more maintainable, easier to understand, and less prone to errors from unused or redundant code.