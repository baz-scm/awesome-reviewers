---
title: prefer simple API designs
description: Design APIs with simple, direct interfaces rather than complex parameter
  passing patterns or unnecessary indirection. Use appropriate parameter types (e.g.,
  `PathFragment` instead of `String`, `ImmutableMap` instead of `BiFunction`) and
  avoid expanding API surface area when existing patterns can be reused.
repository: bazelbuild/bazel
label: API
language: Java
comments_count: 7
repository_stars: 24489
---

Design APIs with simple, direct interfaces rather than complex parameter passing patterns or unnecessary indirection. Use appropriate parameter types (e.g., `PathFragment` instead of `String`, `ImmutableMap` instead of `BiFunction`) and avoid expanding API surface area when existing patterns can be reused.

**Key principles:**
- **Direct method calls over complex parameter passing**: Instead of plumbing arguments through multiple components, create direct API methods like `RunfilesSupport.withExecutableAndArgs()`
- **Appropriate parameter types**: Use domain-specific types (`PathFragment`) rather than generic ones (`String`) for better type safety
- **Minimize API expansion**: Reuse existing patterns and avoid adding new methods when current APIs can be extended consistently
- **Avoid complex function parameters**: Replace complex function types like `BiFunction<ImmutableMap<String, String>, String, ImmutableMap<String, String>>` with direct parameter passing

**Example:**
```java
// Avoid complex function parameters
public CppModuleMapAction(
    // ... other params
    BiFunction<ImmutableMap<String, String>, String, ImmutableMap<String, String>> modifyExecutionInfo) {

// Prefer direct parameter passing
public CppModuleMapAction(
    // ... other params  
    ImmutableMap<String, String> executionInfo) {
```

This approach makes APIs more predictable, easier to test, and reduces the cognitive load on API consumers while maintaining clear contracts between components.