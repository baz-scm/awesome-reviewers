---
title: Use named constants
description: Replace hardcoded string literals and magic values with named constants
  to improve code maintainability and readability. This practice prevents typos, makes
  the code self-documenting, and provides a single source of truth when the same value
  is used in multiple places.
repository: flutter/flutter
label: Code Style
language: Java
comments_count: 2
repository_stars: 172252
---

Replace hardcoded string literals and magic values with named constants to improve code maintainability and readability. This practice prevents typos, makes the code self-documenting, and provides a single source of truth when the same value is used in multiple places.

Instead of using hardcoded strings directly in the code:
```java
String prefix = "--aot-shared-library-name=";
Path pathWithoutSoFile = internalStorageDirAsPathObj.resolve(Paths.get("library.so"));
```

Extract them to meaningful constants:
```java
private static final String AOT_SHARED_LIBRARY_NAME_PREFIX = "--aot-shared-library-name=";
private static final String DEFAULT_LIBRARY_NAME = "library.so";

String prefix = AOT_SHARED_LIBRARY_NAME_PREFIX;
Path pathWithoutSoFile = internalStorageDirAsPathObj.resolve(Paths.get(DEFAULT_LIBRARY_NAME));
```

This approach makes the code more maintainable, reduces duplication, and clearly communicates the purpose of each value through descriptive constant names.