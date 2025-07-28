---
title: avoid unnecessary conversions
description: Choose direct, efficient methods over approaches that require additional
  parsing, conversion, or processing steps. This reduces computational overhead and
  improves performance by eliminating intermediate operations.
repository: facebook/react-native
label: Performance Optimization
language: Kotlin
comments_count: 3
repository_stars: 123178
---

Choose direct, efficient methods over approaches that require additional parsing, conversion, or processing steps. This reduces computational overhead and improves performance by eliminating intermediate operations.

When equivalent alternatives exist, prefer:
- Direct constructors over string parsing (e.g., `Color.rgb(11, 6, 0)` instead of parsing hex strings)
- Native method calls over wrapper methods that add conversion layers
- Conditional execution over forced operations (check if work is needed before performing expensive operations)

Example from code reviews:
```kotlin
// Avoid: String parsing with conversion overhead
val color = if (isDarkMode) "#0b0600" else "#f3f8ff"

// Prefer: Direct constructor
val color = if (isDarkMode) Color.rgb(11, 6, 0) else Color.rgb(243, 248, 255)
```

This principle applies to any situation where you can eliminate intermediate processing steps, type conversions, or unnecessary method calls that don't add functional value but consume computational resources.