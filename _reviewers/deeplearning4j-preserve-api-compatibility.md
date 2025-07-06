---
title: Preserve API compatibility
description: When evolving APIs, prioritize backward compatibility to protect existing
  client code. Make new parameters optional whenever possible to allow existing code
  to continue functioning. If breaking changes are necessary, evaluate how users typically
  interact with your API before proceeding.
repository: deeplearning4j/deeplearning4j
label: API
language: Kotlin
comments_count: 2
repository_stars: 14036
---

When evolving APIs, prioritize backward compatibility to protect existing client code. Make new parameters optional whenever possible to allow existing code to continue functioning. If breaking changes are necessary, evaluate how users typically interact with your API before proceeding.

Example:
```kotlin
// Good: Adding a new parameter with a default value
val reduce = Mixin("reduce"){
    Input(DataType.NUMERIC, "in") { description = "Input variable" }
    // New parameter with default value maintains compatibility
    Arg(DataType.BOOL, "keepDims", default = false) {
        "Whether to keep original dimensions or produce a shrunk array"
    }
    Arg(DataType.INT, "dimensions") { /* ... */ }
}

// Consider impact: Breaking changes may be acceptable if most users
// are protected by higher-level abstractions (e.g., factory methods)
// rather than using these classes directly
```

Breaking changes may be acceptable when most users access functionality through higher-level abstractions (like factory methods) that can shield them from underlying implementation changes. Always document breaking changes clearly in release notes.