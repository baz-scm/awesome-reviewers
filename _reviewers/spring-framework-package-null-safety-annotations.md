---
title: Package null-safety annotations
description: All package-info.java files must include both @NonNullApi and @NonNullFields
  annotations to establish null-safety at the package level. These annotations must
  each be on a single line for proper detection by static analysis tools. This practice
  makes null-handling behavior explicit, reduces NullPointerExceptions, and enforces
  consistent null-safety...
repository: spring-projects/spring-framework
label: Null Handling
language: Xml
comments_count: 3
repository_stars: 58382
---

All package-info.java files must include both @NonNullApi and @NonNullFields annotations to establish null-safety at the package level. These annotations must each be on a single line for proper detection by static analysis tools. This practice makes null-handling behavior explicit, reduces NullPointerExceptions, and enforces consistent null-safety conventions across the codebase.

Example:
```java
/**
 * Package documentation here.
 */
@NonNullApi
@NonNullFields
package com.example.mypackage;

import org.springframework.lang.NonNullApi;
import org.springframework.lang.NonNullFields;
```