---
title: Wrap and check errors
description: Always wrap errors with meaningful context and use typed error checking
  instead of string matching. This helps with error tracing and maintains consistent
  error handling patterns.
repository: docker/compose
label: Error Handling
language: Go
comments_count: 4
repository_stars: 35858
---

Always wrap errors with meaningful context and use typed error checking instead of string matching. This helps with error tracing and maintains consistent error handling patterns.

Key practices:
1. Use `errors.Wrap()` or `fmt.Errorf()` with `%w` to preserve error chains
2. Leverage typed error checking functions like `errdefs.IsNotFound()`
3. Provide clear, actionable error messages

Example:

```go
// Bad:
if err != nil && strings.HasPrefix(err.Error(), "no container found") {
    return nil
}

// Good:
if err != nil {
    if errdefs.IsNotFound(err) {
        return nil
    }
    return fmt.Errorf("failed to create volume %q: %w", name, err)
}

// Bad:
return fmt.Errorf("volume %q exists but not created by Compose", name)

// Good:
return fmt.Errorf("volume %q already exists but was not created by Docker Compose. Use `external: true` to use an existing volume", name)
```