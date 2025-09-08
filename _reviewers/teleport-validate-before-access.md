---
title: validate before access
description: Always check for null, empty, or unset values before accessing or processing
  them, and return meaningful errors when validation fails. This prevents runtime
  panics and provides clear feedback about missing required data.
repository: gravitational/teleport
label: Null Handling
language: Go
comments_count: 2
repository_stars: 19109
---

Always check for null, empty, or unset values before accessing or processing them, and return meaningful errors when validation fails. This prevents runtime panics and provides clear feedback about missing required data.

When accessing potentially null or empty values, implement explicit validation:

```go
// Check for empty parameters
params := q.Get("params")
if params == "" {
    return nil, trace.BadParameter("missing params")
}

// Check for nil context values  
func (ctx *Context) GetRole() (types.Role, error) {
    if ctx.role == nil {
        return nil, trace.NotFound("role is not set in the context")
    }
    return ctx.role, nil
}
```

This pattern ensures that null or empty states are caught early with descriptive error messages, rather than allowing them to propagate and cause unexpected behavior or panics later in the code execution.