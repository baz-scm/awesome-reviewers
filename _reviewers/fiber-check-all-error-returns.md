---
title: check all error returns
description: Always check and handle error returns from function calls, even for operations
  that seem unlikely to fail. Ignoring errors can lead to silent failures, resource
  leaks, and unpredictable behavior in production.
repository: gofiber/fiber
label: Error Handling
language: Go
comments_count: 7
repository_stars: 37560
---

Always check and handle error returns from function calls, even for operations that seem unlikely to fail. Ignoring errors can lead to silent failures, resource leaks, and unpredictable behavior in production.

Common patterns to avoid:
- Missing error checks: `ln.Close()` without checking the error
- Silent error ignoring: returning without handling errors from critical operations
- Assuming operations never fail: even operations like certificate parsing can fail

Proper error handling patterns:
- Check errors immediately after function calls
- Use early returns to avoid unnecessary processing when errors occur
- Log errors appropriately before returning or handling them
- For operations in defer statements, still check errors when meaningful

Example of missing error check:
```go
// Bad: Missing error check
file, err := os.Open(path)
if err != nil {
    return err
}
defer file.Close() // Error ignored

// Good: Proper error handling
file, err := os.Open(path)
if err != nil {
    return err
}
defer func() {
    if closeErr := file.Close(); closeErr != nil {
        log.Errorf("failed to close file: %v", closeErr)
    }
}()
```

Example of early error return:
```go
// Bad: Continuing processing after error
key, err := parseParamSquareBrackets(key)
// ... rest of function continues regardless

// Good: Early error return
key, err := parseParamSquareBrackets(key)
if err != nil {
    return err
}
// ... continue processing
```

This practice is essential for building robust applications that handle failure scenarios gracefully and provide meaningful error information for debugging.