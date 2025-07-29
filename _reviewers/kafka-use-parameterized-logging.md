---
title: Use parameterized logging
description: Use parameterized logging with placeholders (`{}`) instead of string
  concatenation for better performance and readability. When logging exceptions, pass
  the exception object as a separate parameter to the logger rather than including
  its message in the format string.
repository: apache/kafka
label: Logging
language: Java
comments_count: 3
repository_stars: 30575
---

Use parameterized logging with placeholders (`{}`) instead of string concatenation for better performance and readability. When logging exceptions, pass the exception object as a separate parameter to the logger rather than including its message in the format string.

**Why this matters:**
- Parameterized logging avoids unnecessary string concatenation when the log level is disabled
- Exception objects as separate parameters provide full stack traces and better debugging information
- Cleaner, more readable code that follows logging framework best practices

**Examples:**

❌ **Avoid string concatenation:**
```java
logger.debug("Fail to read the clean shutdown file in " + cleanShutdownFile.toPath() + ":" + e);
LOGGER.error(format("Encountered error while deleting %s", file.getAbsolutePath()));
```

✅ **Use parameterized logging:**
```java
logger.debug("Fail to read the clean shutdown file in {}:{}", cleanShutdownFile.toPath(), e);
LOGGER.error("Encountered error while deleting {}", file.getAbsolutePath(), e);
```

❌ **Avoid including exception message in format string:**
```java
String msg = String.format("Deserializing record %s from %s failed due to: %s", record, tp, ex.getMessage());
LOG.error(msg);
```

✅ **Pass exception as separate parameter:**
```java
String msg = String.format("Deserializing record %s from %s failed", record, tp);
LOG.error(msg, ex);
```

This approach ensures optimal performance, provides complete exception information, and maintains consistent logging patterns across the codebase.