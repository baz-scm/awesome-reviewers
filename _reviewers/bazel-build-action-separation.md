---
title: build action separation
description: Keep build actions focused on their core responsibility and move complex
  logic to appropriate abstraction layers like builders or configuration components.
  Build actions should contain minimal action-specific branching and avoid tight coupling
  to implementation details.
repository: bazelbuild/bazel
label: CI/CD
language: Java
comments_count: 4
repository_stars: 24489
---

Keep build actions focused on their core responsibility and move complex logic to appropriate abstraction layers like builders or configuration components. Build actions should contain minimal action-specific branching and avoid tight coupling to implementation details.

This principle improves build system maintainability and reliability in CI/CD pipelines by:
- Making actions easier to debug when builds fail
- Reducing complexity that can lead to unpredictable behavior
- Enabling better separation of concerns for different build phases
- Avoiding architectural decisions that make the system harder to extend

For example, instead of adding conditional logic directly in a compile action:

```java
// Avoid: Complex branching in action
if (featureConfiguration.isEnabled(CppRuleClasses.CPP_MODULES)) {
  if (dotdFile != null) {
    outputs.add(dotdFile);
  }
}
```

Move the logic to the builder where it belongs:

```java
// Prefer: Logic in builder, clean action
// Builder handles the conditional logic
// Action just processes what builder provides
```

Similarly, avoid introducing special artifacts or complex coupling that makes the build system "un-Starlarkifiable" or harder to maintain. When build actions stay focused and delegate complex decisions to appropriate layers, the entire CI/CD pipeline becomes more reliable and easier to troubleshoot.