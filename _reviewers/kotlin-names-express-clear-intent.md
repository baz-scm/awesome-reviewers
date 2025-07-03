---
title: Names express clear intent
description: Choose names that clearly express intent and follow established conventions.
  Prefer explicit, descriptive names over abbreviations or ambiguous terms. Align
  with platform-specific naming patterns and maintain consistency with existing codebase
  conventions.
repository: JetBrains/kotlin
label: Naming Conventions
language: Kotlin
comments_count: 11
repository_stars: 50857
---

Choose names that clearly express intent and follow established conventions. Prefer explicit, descriptive names over abbreviations or ambiguous terms. Align with platform-specific naming patterns and maintain consistency with existing codebase conventions.

Key guidelines:
- Use full descriptive names instead of abbreviations (e.g., `BREADTH_FIRST` over `BFS`)
- Follow platform naming conventions (e.g., `reifiedTypeParameters` for properties, `getReifiedTypeParameters()` for functions in Kotlin)
- Choose names that accurately reflect the variable's purpose (e.g., `argumentType` instead of `typeArgument`)
- Avoid terms that conflict with language keywords or have special meaning (e.g., use `child` instead of `inner`)
- Maintain consistency with similar names in the codebase

Example:
```kotlin
// Incorrect
enum class WalkAlgorithm {
    BFS,  // Abbreviated
    DFS   // Abbreviated
}

// Correct
enum class WalkAlgorithm {
    BREADTH_FIRST,  // Explicit
    DEPTH_FIRST    // Explicit
}
```
