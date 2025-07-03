---
title: Standardize build configurations
description: 'Maintain consistent and standardized build configurations across the
  project to improve maintainability and reduce errors:


  1. **Centralize dependency management** - Use shared dependency declarations rather
  than hardcoding versions in individual module build files. This ensures consistency
  across the project and makes version updates simpler.'
repository: JetBrains/kotlin
label: Configurations
language: Other
comments_count: 3
repository_stars: 50857
---

Maintain consistent and standardized build configurations across the project to improve maintainability and reduce errors:

1. **Centralize dependency management** - Use shared dependency declarations rather than hardcoding versions in individual module build files. This ensures consistency across the project and makes version updates simpler.

   ```gradle
   // Instead of:
   testImplementation("com.google.code.gson:gson:2.8.9")
   
   // Prefer using centralized dependency management:
   testImplementation(commonDependency("com.google.code.gson:gson"))
   ```

2. **Avoid duplicating configurations** - Don't repeat configuration code that's already defined in parent or root projects. Reference or inherit from common configurations instead.

3. **Prefer Kotlin DSL** - For new modules, use `.gradle.kts` (Kotlin) scripts rather than `.gradle` (Groovy) scripts to benefit from type safety, better IDE support, and consistency with the broader codebase.

By following these practices, you'll reduce configuration drift, make updates more manageable, and maintain a more consistent build environment.
