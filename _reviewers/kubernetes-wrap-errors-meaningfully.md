---
title: Wrap errors meaningfully
description: 'Always wrap errors with meaningful context that explains what operation
  failed and why. Use proper error wrapping with `fmt.Errorf("operation failed: %w",
  err)` to preserve the original error chain while adding context. Include explanatory
  comments for complex error handling logic to clarify the intended behavior and recovery
  strategy.'
repository: kubernetes/kubernetes
label: Error Handling
language: Go
comments_count: 4
repository_stars: 116489
---

Always wrap errors with meaningful context that explains what operation failed and why. Use proper error wrapping with `fmt.Errorf("operation failed: %w", err)` to preserve the original error chain while adding context. Include explanatory comments for complex error handling logic to clarify the intended behavior and recovery strategy.

When handling timeouts, wrap with specific timeout context:
```go
if err != nil {
    if errors.Is(err, context.DeadlineExceeded) {
        err = fmt.Errorf("device binding timeout: %w", err)
    }
    return statusError(logger, err)
}
```

Add comments to explain error handling decisions:
```go
// Returning an error here causes another scheduling attempt.
// In that next attempt, PreFilter will detect the timeout or
// error and try to recover.
return statusError(logger, err)
```

Make error messages descriptive and mention relevant context like retry attempts, duration, or affected resources. This helps with debugging and provides actionable information for both developers and operators.