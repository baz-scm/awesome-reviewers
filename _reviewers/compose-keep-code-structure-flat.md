---
title: Keep code structure flat
description: 'Maintain code readability by minimizing nesting depth and using appropriate
  control structures. Prefer flat code organization over deeply nested conditions.
  When dealing with multiple conditions:'
repository: docker/compose
label: Code Style
language: Go
comments_count: 4
repository_stars: 35858
---

Maintain code readability by minimizing nesting depth and using appropriate control structures. Prefer flat code organization over deeply nested conditions. When dealing with multiple conditions:

1. Invert if statements to handle edge cases early
2. Use switch statements for multiple related conditions
3. Structure code to make the logic flow obvious

Example - Instead of:
```go
if condition {
    if nestedCondition {
        for name, s := range items {
            if deeplyNested {
                // actual logic
            }
        }
    }
}
```

Prefer:
```go
if !condition {
    return
}
if !nestedCondition {
    return
}
switch {
case condition1:
    // handle case
case condition2:
    // handle case
default:
    // handle default
}
```

This approach improves code readability, reduces cognitive load, and makes the code easier to maintain and debug.