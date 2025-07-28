---
title: prefer system properties directly
description: When detecting operating system or environment characteristics, prefer
  direct access to system properties over external library dependencies for basic
  checks. Use `System.getProperty("os.name")` with `regionMatches()` for case-insensitive
  OS detection instead of relying on third-party utilities like Apache Commons Lang3's
  SystemUtils.
repository: apache/spark
label: Configurations
language: Java
comments_count: 2
repository_stars: 41554
---

When detecting operating system or environment characteristics, prefer direct access to system properties over external library dependencies for basic checks. Use `System.getProperty("os.name")` with `regionMatches()` for case-insensitive OS detection instead of relying on third-party utilities like Apache Commons Lang3's SystemUtils.

This approach reduces external dependencies while maintaining equivalent functionality. The `regionMatches()` method provides robust, case-insensitive string matching that handles OS name variations effectively.

Example implementation:
```java
// Instead of: SystemUtils.IS_OS_WINDOWS
boolean isWindows = System.getProperty("os.name").regionMatches(true, 0, "Windows", 0, 7);

// Instead of: SystemUtils.IS_OS_UNIX  
String osName = System.getProperty("os.name");
String[] unixPrefixes = {"AIX", "HP-UX", "Linux", "Mac OS X", "Solaris", "FreeBSD"};
boolean isUnix = Arrays.stream(unixPrefixes)
    .anyMatch(prefix -> osName.regionMatches(true, 0, prefix, 0, prefix.length()));
```

This pattern is particularly valuable when the external library is used minimally and the custom implementation can be easily maintained and tested.