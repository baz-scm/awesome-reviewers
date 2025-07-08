---
title: Reduce code nesting
description: Minimize nesting levels and complexity in your code to improve readability
  and maintainability. Use early returns instead of deeply nested conditions, and
  restructure switch statements to reduce complexity.
repository: opentofu/opentofu
label: Code Style
language: Go
comments_count: 6
repository_stars: 25901
---

Minimize nesting levels and complexity in your code to improve readability and maintainability. Use early returns instead of deeply nested conditions, and restructure switch statements to reduce complexity.

Here are practical approaches to reduce nesting:

1. **Use early returns for error conditions or special cases:**
```go
// Instead of this:
if condition {
    // Long code block here
    if anotherCondition {
        // More code here
    }
}

// Do this:
if !condition {
    return // or handle the error case
}
// Long code block here
if !anotherCondition {
    return // or handle the error case
}
// More code here
```

2. **Simplify switch statements:**
```go
// Instead of nested switch-case:
switch {
case !forEachVal.IsKnown():
    if !allowUnknown {
        var detailMsg string
        switch {
        case ty.IsSetType():
            detailMsg = errInvalidUnknownDetailSet
        default:
            detailMsg = errInvalidUnknownDetailMap
        }
        // Handle error...
    }
    
// Use simpler pattern with clear, separated checks:
if !forEachVal.IsKnown() && !allowUnknown {
    var detailMsg string
    if ty.IsSetType() {
        detailMsg = errInvalidUnknownDetailSet
    } else {
        detailMsg = errInvalidUnknownDetailMap
    }
    // Handle error...
    return // early return after error handling
}
```

3. **Extract complex logic into helper functions** with clear names to reduce the depth of your primary functions.

4. **For conditional logic, use clear variable names** instead of nested expressions to improve readability:
```go
// Instead of:
if ext := tfFileExt(p); ext != "" {
    parallelTofuExt := strings.ReplaceAll(ext, ".tf", ".tofu")
    pathWithoutExt, _ := strings.CutSuffix(p, ext)
    parallelTofuPath := pathWithoutExt + parallelTofuExt
    // Nested logic here...
} else {
    relevantPaths = append(relevantPaths, p)
}

// Do this:
ext := tfFileExt(p)
if ext == "" {
    relevantPaths = append(relevantPaths, p)
    continue
}

parallelTofuExt := strings.ReplaceAll(ext, ".tf", ".tofu")
pathWithoutExt, _ := strings.CutSuffix(p, ext)
parallelTofuPath := pathWithoutExt + parallelTofuExt
// Logic continues with less nesting...
```

These changes make code easier to follow, test, and maintain.