---
title: Minimize code nesting depth
description: Reduce cognitive load and improve code readability by minimizing nested
  code blocks. Prefer early returns and flattened logic over deeply nested conditions.
  This makes the code easier to read, understand, and maintain.
repository: temporalio/temporal
label: Code Style
language: Go
comments_count: 3
repository_stars: 14953
---

Reduce cognitive load and improve code readability by minimizing nested code blocks. Prefer early returns and flattened logic over deeply nested conditions. This makes the code easier to read, understand, and maintain.

Example - Instead of nested conditions:
```go
func foo() {
    result, err = tryA()
    if err != nil { 
        result, err = tryB()
        if err != nil { 
            result, err = tryC() 
            if err != nil {
                return nil, custom_error
            }
        }
    } 
    return result, err
}
```

Prefer flattened logic:
```go
func foo() {
    result, err = tryA()
    if err == nil { 
        return result, nil
    }
    
    result, err = tryB()
    if err == nil { 
        return result, nil
    }

    result, err = tryC()
    if err == nil { 
        return result, nil
    }

    return nil, custom_error
}
```

Key benefits:
- Reduces cognitive load when reading code
- Makes the logical flow more obvious
- Easier to add or modify conditions
- Improves code maintainability

Note: While reducing nesting is generally beneficial, consider maintaining clear logical grouping when it helps tell the code's story. The goal is to balance readability with logical clarity.