---
title: Clear recoverable error messages
description: 'Error messages should be clear, actionable, and indicate whether recovery
  is possible. When designing error handling:


  1. Use descriptive messages that explain what went wrong and how to fix it'
repository: ollama/ollama
label: Error Handling
language: Go
comments_count: 5
repository_stars: 145704
---

Error messages should be clear, actionable, and indicate whether recovery is possible. When designing error handling:

1. Use descriptive messages that explain what went wrong and how to fix it
2. Indicate if the error is expected/recoverable
3. Provide appropriate fallbacks when safe
4. Include relevant context in error messages

Example:

```go
// Instead of
if err != nil {
    return fmt.Errorf("puller failed: %w", err)
}

// Do this
if err != nil {
    if errors.Is(err, ErrModelNotFound) {
        // Clear message with actionable hint
        return fmt.Errorf("model %q not found - check available models at: https://ollama.com/models", name)
    }
    // Indicate if retry may help
    if isTemporary(err) {
        return fmt.Errorf("temporary error fetching model %q, retry may resolve: %w", name, err)
    }
    return fmt.Errorf("failed to pull model %q: %w", name, err)
}

// Consider fallbacks for non-critical errors
if req.Options == nil {
    // Use safe defaults instead of error
    req.Options = api.DefaultOptions()
}
```

This approach helps users understand and recover from errors while maintaining system stability through appropriate fallbacks.