---
title: Use configuration property providers
description: Always use Gradle's Provider API when accessing project, system, or Gradle
  properties in your build configuration. This ensures proper handling of configuration
  cache and allows for dynamic property updates.
repository: JetBrains/kotlin
label: Configurations
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Always use Gradle's Provider API when accessing project, system, or Gradle properties in your build configuration. This ensures proper handling of configuration cache and allows for dynamic property updates.

Instead of directly accessing properties:

```kotlin
// DON'T
val verbose = (project.hasProperty("kapt.verbose") && 
    project.property("kapt.verbose").toString().toBoolean() == true)

// DO
val verbose = project.providers.gradleProperty("kapt.verbose")
    .map { it.toBoolean() }
    .orElse(false)

// DON'T
val systemProp = System.getProperty("my.property")

// DO
val systemProp = project.providers.systemProperty("my.property")
```

This approach:
- Supports Gradle's configuration cache feature
- Allows for property value changes during build execution
- Provides proper lazy evaluation of properties
- Maintains build configuration stability

When dealing with file paths or build directory locations, use ProjectLayout:
```kotlin
val layout = project.layout
val outputFile = layout.buildDirectory.file("output/file.txt")
```
