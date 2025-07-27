---
title: Optimize variable declarations
description: Declare variables close to their usage point and choose appropriate types
  to improve code readability and reduce cognitive load. Avoid declaring variables
  at the top of functions when they're only used once later in the code. Remove unused
  variables and imports to keep the codebase clean.
repository: snyk/cli
label: Code Style
language: Go
comments_count: 4
repository_stars: 5178
---

Declare variables close to their usage point and choose appropriate types to improve code readability and reduce cognitive load. Avoid declaring variables at the top of functions when they're only used once later in the code. Remove unused variables and imports to keep the codebase clean.

Key practices:
- Declare variables where they are first used rather than at function start
- Use appropriate types (e.g., boolean instead of integer for flags)
- Remove unused variables and imports immediately
- Avoid unnecessary variable assignments when the value is available elsewhere

Example of improvement:
```go
// Instead of declaring at top:
func updateConfigFromParameter(config configuration.Configuration, args []string, rawArgs []string) {
    doubleDashArgs := []string{}
    doubleDashPosition := -1  // could be boolean
    // ... later usage
}

// Declare where used with appropriate type:
func updateConfigFromParameter(config configuration.Configuration, args []string, rawArgs []string) {
    // ... other code
    doubleDashArgs := []string{}
    foundDoubleDash := false  // boolean is clearer than position integer
    // ... immediate usage
}
```

This practice reduces the mental overhead of tracking variable scope and purpose, making code easier to understand and maintain.