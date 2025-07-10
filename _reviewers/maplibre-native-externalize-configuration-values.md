---
title: Externalize configuration values
description: Use environment variables and external configuration mechanisms instead
  of hard-coding values in build scripts. This makes your build system more flexible,
  maintainable, and adaptable to different environments.
repository: maplibre/maplibre-native
label: Configurations
language: Kotlin
comments_count: 3
repository_stars: 1411
---

Use environment variables and external configuration mechanisms instead of hard-coding values in build scripts. This makes your build system more flexible, maintainable, and adaptable to different environments.

**Why it matters:**
- Hard-coded values like file paths (e.g., `/usr/bin/ccache`) limit where tools can be installed
- Project-specific constraints (e.g., spaces in project names causing Dokka errors) should be externalized
- Configuration options should be adaptable across different environments

**How to implement:**
1. Replace hard-coded paths with environment variable lookups
2. Use properties files or command-line parameters for configurable values
3. Document configuration requirements clearly

**Example:**
Instead of:
```kotlin
// Hard-coded paths that limit where ccache can be installed
val ccachePaths = listOf("/usr/bin/ccache", "/usr/local/bin/ccache")
```

Better approach:
```kotlin
// Use environment variables with fallbacks
val ccachePath = System.getenv("CCACHE_PATH") 
    ?: listOf("/usr/bin/ccache", "/usr/local/bin/ccache").firstOrNull { file(it).exists() }

if (ccachePath != null) {
    arguments("-DANDROID_CCACHE=$ccachePath")
}
```

Similarly, for dependency exclusions, use a consistent pattern:
```kotlin
configurations {
    getByName("implementation") {
        exclude(group = "commons-logging", module = "commons-logging")
        exclude(group = "commons-collections", module = "commons-collections")
    }
}
```