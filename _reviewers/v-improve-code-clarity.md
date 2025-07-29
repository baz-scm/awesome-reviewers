---
title: Improve code clarity
description: Write code that clearly expresses intent through explicit patterns, simplified
  logic, and readable structure. Avoid unnecessary complexity that obscures the code's
  purpose.
repository: vlang/v
label: Code Style
language: Other
comments_count: 10
repository_stars: 36582
---

Write code that clearly expresses intent through explicit patterns, simplified logic, and readable structure. Avoid unnecessary complexity that obscures the code's purpose.

Key practices:
- **Eliminate unnecessary nesting**: When an if block returns, omit the else block to reduce indentation levels
- **Simplify verbose conditionals**: Replace `if condition { return true } else { return false }` with `return condition`
- **Be explicit about ignored values**: Use `_ = function_call()` instead of just `function_call()` when intentionally ignoring return values
- **Move variables close to usage**: Declare variables near where they're used rather than at distant locations
- **Avoid unnecessary complexity**: Don't use closures, string interpolation, or complex patterns when simpler alternatives exist
- **Use clear function signatures**: Always include parameter names in function declarations for better readability

Example of improvement:
```v
// Before: verbose and nested
pub fn (s Status) is_success() bool {
    if s.status.is_success() {
        return true
    } else {
        return false
    }
}

// After: clear and direct  
pub fn (s Status) is_success() bool {
    return s.status.is_success()
}
```

This approach makes code easier to read, understand, and maintain by reducing cognitive load and making intentions explicit.