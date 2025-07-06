---
title: Extract repeated code
description: Identify and extract repeated code patterns into well-named functions
  to improve readability, maintainability, and testability. Look for blocks of code
  that appear in multiple places or complex operations that can be encapsulated with
  a descriptive function name.
repository: grafana/grafana
label: Code Style
language: Go
comments_count: 9
repository_stars: 68825
---

Identify and extract repeated code patterns into well-named functions to improve readability, maintainability, and testability. Look for blocks of code that appear in multiple places or complex operations that can be encapsulated with a descriptive function name.

**Examples:**

1. For repetitive test setup code:
```go
// Instead of repeating this in multiple test functions:
testObj, err := createTestObject()
require.NoError(t, err)
metaAccessor, err := utils.MetaAccessor(testObj)
require.NoError(t, err)
writeEvent := WriteEvent{...}

// Create a helper function:
func writeObject(t *testing.T, backend *Backend, testObj Object) {
    metaAccessor, err := utils.MetaAccessor(testObj)
    require.NoError(t, err)
    writeEvent := WriteEvent{...}
    // etc.
}
```

2. For common API patterns with similar behavior:
```go
// Instead of repeating client initialization logic:
func NewResourceClient(conn grpc.ClientConnInterface) ResourceClient {
    return &resourceClient{...}
}

func NewAuthlessResourceClient(cc grpc.ClientConnInterface) ResourceClient {
    return newResourceClient(cc)
}

func NewLegacyResourceClient(cc grpc.ClientConnInterface) ResourceClient {
    return newResourceClient(cc)
}
```

3. For instrumentation code:
```go
// Instead of repeating timing and metrics in each CRUD method:
func (s *store) withMetrics(ctx context.Context, operation string, fn func() error) error {
    start := time.Now()
    err := fn()
    s.metrics.ObserveOperation(operation, time.Since(start), err == nil)
    return err
}
```

This approach makes the main code paths clearer, easier to maintain, and reduces the risk of inconsistencies. When extracting functions, use descriptive names that indicate what the function does rather than how it works.