---
title: Use idiomatic Go flow
description: 'Follow Go''s idiomatic control flow patterns to improve code readability
  and maintainability. Key practices include:


  1. Prefer early returns over else blocks'
repository: ollama/ollama
label: Code Style
language: Go
comments_count: 5
repository_stars: 145704
---

Follow Go's idiomatic control flow patterns to improve code readability and maintainability. Key practices include:

1. Prefer early returns over else blocks
2. Return errors on the right in function signatures
3. Use if statements instead of switches for single cases

Example - Before:
```go
func inferThinkingOption(caps *[]model.Capability, runOpts *runOptions, explicitlySetByUser bool) (error, *bool) {
    if condition {
        // success case
    } else {
        return errors.New("error"), nil
    }
}
```

After:
```go
func inferThinkingOption(caps *[]model.Capability, runOpts *runOptions, explicitlySetByUser bool) (*bool, error) {
    if !condition {
        return nil, errors.New("error")
    }
    // success case
}
```

This approach:
- Makes code flow more predictable
- Reduces nesting and cognitive load
- Follows established Go conventions
- Makes error handling more consistent