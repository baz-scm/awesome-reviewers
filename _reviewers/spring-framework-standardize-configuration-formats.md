---
title: Standardize configuration formats
description: 'Use consistent, explicit, and well-documented formats in all configuration
  files to improve readability and prevent misunderstandings. When defining configuration
  values:'
repository: spring-projects/spring-framework
label: Configurations
language: Other
comments_count: 3
repository_stars: 58382
---

Use consistent, explicit, and well-documented formats in all configuration files to improve readability and prevent misunderstandings. When defining configuration values:

1. Use consistent units for numerical values (e.g., prefer `2g` instead of `2048m` for memory settings)
2. Explicitly configure all necessary goals/options for build tools rather than relying on defaults
3. Be specific about file type configurations when appropriate rather than using overly broad wildcards

Example:
```gradle
// Gradle properties - consistent format for memory
org.gradle.jvmargs=-Xmx2g

// Build configurations - explicit plugin configuration
plugins {
    id 'io.spring.javaformat' version "${javaFormatVersion}"
}

// Explicitly configure all required tasks
tasks.named('format') {
    // Configuration here
}

// Editor configurations - specific rather than overly broad when needed
// .editorconfig example with targeted file types
[*.{java,xml,properties}]
charset = utf-8
```

Following these practices ensures configs are more maintainable, easier to understand at a glance, and less prone to unexpected behavior.