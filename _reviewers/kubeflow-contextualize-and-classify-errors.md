---
title: Contextualize and classify errors
description: Always provide meaningful context when handling errors, and classify
  them appropriately based on their source. This improves debugging, helps users understand
  issues, and creates a consistent approach to error handling across the codebase.
repository: kubeflow/kubeflow
label: Error Handling
language: Go
comments_count: 4
repository_stars: 15064
---

Always provide meaningful context when handling errors, and classify them appropriately based on their source. This improves debugging, helps users understand issues, and creates a consistent approach to error handling across the codebase.

Follow these error handling principles:

1. **Use early returns with clear error checks**:
```go
if err != nil {
    // Log error and/or return response
    return nil, fmt.Errorf("failed to process request: %v", err)
}
// Handle the success case
```

2. **Provide context in error messages**:
```go
// Instead of just returning or logging the raw error
if _, err := w.Write([]byte(err.Error())); err != nil {
    log.Error(err) // Poor context

    // Better approach with context
    log.Error(fmt.Errorf("failed to write error response: %v", err))
}
```

3. **Distinguish between error variables in nested scopes**:
```go
err := json.NewDecoder(r.Body).Decode(&profile)
if err != nil {
    // Handle first error
    if writeErr := json.NewEncoder(w).Encode(err); writeErr != nil {
        log.Error(fmt.Errorf("decode failed: %v, response write failed: %v", err, writeErr))
    }
    return
}
```

4. **Classify errors properly**:
```go
// For user input errors
return &kfapis.KfError{
    Code:    int(kfapis.INVALID_ARGUMENT),
    Message: fmt.Sprintf("Project not specified: %v", err),
}

// For system/internal errors
return &kfapis.KfError{
    Code:    int(kfapis.INTERNAL_ERROR),
    Message: fmt.Sprintf("Failed to create application: %v", err),
}
```

5. **Use consistent error types** throughout your codebase, and consider creating helper functions to reduce boilerplate:
```go
func NewInvalidArgumentError(err error, msg string) *kfapis.KfError {
    return &kfapis.KfError{
        Code:    int(kfapis.INVALID_ARGUMENT),
        Message: fmt.Sprintf("%s: %v", msg, err),
    }
}
```
