---
title: Handle all errors explicitly
description: Always explicitly handle errors rather than assuming they are handled
  by dependencies or ignoring them. Every function that returns an error should have
  that error checked and handled appropriately. Use proper error wrapping with fmt.Errorf
  and the %w verb to maintain error chains, and ensure resource cleanup with defer
  statements even when errors occur.
repository: snyk/cli
label: Error Handling
language: Go
comments_count: 7
repository_stars: 5178
---

Always explicitly handle errors rather than assuming they are handled by dependencies or ignoring them. Every function that returns an error should have that error checked and handled appropriately. Use proper error wrapping with fmt.Errorf and the %w verb to maintain error chains, and ensure resource cleanup with defer statements even when errors occur.

Key practices:
- Check all error returns, even from seemingly safe operations like regex matching
- Use explicit if/else blocks instead of assuming error handling happens elsewhere
- Wrap errors with context using fmt.Errorf("operation failed: %w", err)
- Use defer for cleanup operations to ensure they execute even with panics/errors
- Avoid ignoring errors with blank identifiers unless absolutely necessary

Example:
```go
// Bad - assuming error is handled elsewhere
match, _ := regexp.MatchString("^[a-zA-Z0-9-]+$", name)

// Good - explicit error handling
match, err := regexp.MatchString("^[a-zA-Z0-9-]+$", name)
if err != nil {
    log.Fatal(err)
}

// Bad - complex defer with ignored error
defer func(Body io.ReadCloser) {
    err := Body.Close()
    if err != nil {
        // empty
    }
}(resp.Body)

// Good - simple defer
defer resp.Body.Close()

// Good - proper error wrapping
if err != nil {
    return fmt.Errorf("failed to create cache directory: %w", err)
}
```

This approach prevents silent failures, makes debugging easier, and ensures robust error handling throughout the codebase.