---
title: Alphabetical ordering requirement
description: Always maintain alphabetical ordering for lists of elements including
  dependencies, modules, configuration entries, and other similar collections. This
  convention improves code organization, makes it easier to locate items, prevents
  duplications, and ensures consistency across the codebase.
repository: spring-projects/spring-boot
label: Code Style
language: Other
comments_count: 6
repository_stars: 77637
---

Always maintain alphabetical ordering for lists of elements including dependencies, modules, configuration entries, and other similar collections. This convention improves code organization, makes it easier to locate items, prevents duplications, and ensures consistency across the codebase.

When adding new elements to existing lists, ensure they are placed in the correct alphabetical position:

```gradle
dependencies {
  // Correct: alphabetically ordered
  dockerTestRuntimeOnly("com.ibm.db2:jcc")
  dockerTestRuntimeOnly("io.r2dbc:r2dbc-mssql")
  dockerTestRuntimeOnly("org.postgresql:postgresql")
  dockerTestRuntimeOnly("org.postgresql:r2dbc-postgresql")
  
  // Incorrect: not alphabetically ordered
  dockerTestRuntimeOnly("io.r2dbc:r2dbc-mssql")
  dockerTestRuntimeOnly("org.postgresql:postgresql")
  dockerTestRuntimeOnly("org.postgresql:r2dbc-postgresql")
  dockerTestRuntimeOnly("com.ibm.db2:jcc")  // Wrong position
}
```

This rule applies to all list-like structures including gradle dependencies, spring.factories entries, module definitions, and similar configuration files throughout the project.