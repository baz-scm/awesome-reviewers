---
title: Prefer early returns
description: Use early returns and guard clauses to reduce nesting levels and improve
  code readability. Instead of deeply nested if-else structures, invert conditions
  and return early when possible. This pattern makes the main logic flow more apparent
  and reduces cognitive load.
repository: argoproj/argo-cd
label: Code Style
language: Go
comments_count: 6
repository_stars: 20149
---

Use early returns and guard clauses to reduce nesting levels and improve code readability. Instead of deeply nested if-else structures, invert conditions and return early when possible. This pattern makes the main logic flow more apparent and reduces cognitive load.

Examples of this pattern:

```go
// Instead of deep nesting:
func processData(data []string) error {
    if len(data) > 0 {
        if isValid(data) {
            // main logic here
            return process(data)
        } else {
            return errors.New("invalid data")
        }
    } else {
        return errors.New("no data")
    }
}

// Prefer early returns:
func processData(data []string) error {
    if len(data) == 0 {
        return errors.New("no data")
    }
    if !isValid(data) {
        return errors.New("invalid data")
    }
    // main logic here
    return process(data)
}
```

This approach is particularly beneficial when functions grow in size or when dealing with multiple validation conditions. It follows Go idioms and makes error handling more explicit while keeping the happy path unindented.