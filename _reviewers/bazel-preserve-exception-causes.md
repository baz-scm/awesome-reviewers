---
title: preserve exception causes
description: When catching an exception and re-throwing a different exception type,
  always preserve the original exception as the cause. This maintains the full stack
  trace and context, making debugging significantly easier.
repository: bazelbuild/bazel
label: Error Handling
language: Java
comments_count: 4
repository_stars: 24489
---

When catching an exception and re-throwing a different exception type, always preserve the original exception as the cause. This maintains the full stack trace and context, making debugging significantly easier.

Swallowing the original exception by not setting it as a cause breaks the error chain and hides valuable debugging information about the root cause of the failure.

**Bad:**
```java
try {
  return Long.parseUnsignedLong(string);
} catch (NumberFormatException e) {
  throw new ParseException("identifier is too large");  // Lost original cause!
}
```

**Good:**
```java
try {
  return Long.parseUnsignedLong(string);
} catch (NumberFormatException e) {
  throw new ParseException("identifier is too large", e);  // Preserves cause
}
```

For custom exceptions that don't accept a cause parameter, use `initCause()`:
```java
try {
  // some operation
} catch (IOException e) {
  CustomException custom = new CustomException("operation failed");
  custom.initCause(e);
  throw custom;
}
```

This practice is especially important in complex systems where exceptions may be caught and re-thrown multiple times through different layers, as each layer can add context while preserving the original root cause.