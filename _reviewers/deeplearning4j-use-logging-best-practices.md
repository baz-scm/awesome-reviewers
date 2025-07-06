---
title: Use logging best practices
description: 'Adopt these logging best practices to ensure consistent, efficient,
  and meaningful logs:


  1. **Use Lombok''s `@Slf4j` annotation** instead of manually declaring loggers:'
repository: deeplearning4j/deeplearning4j
label: Logging
language: Java
comments_count: 5
repository_stars: 14036
---

Adopt these logging best practices to ensure consistent, efficient, and meaningful logs:

1. **Use Lombok's `@Slf4j` annotation** instead of manually declaring loggers:

```java
// Avoid this:
private static final Logger log = LoggerFactory.getLogger(YourClass.class);

// Prefer this:
@Slf4j
public class YourClass {
    // Logger field 'log' is automatically created
}
```

2. **Choose appropriate log levels** based on the information's importance:
   - `log.trace()`: Very detailed information, typically only valuable when debugging specific issues
   - `log.debug()`: Development-time information like "Stringing exec...", "exec done."
   - `log.info()`: Production-worthy information about application progress
   - `log.warn()`: Potential issues that don't prevent operation
   - `log.error()`: Actual failures requiring attention

3. **Log exceptions properly** by passing the exception object as an argument:

```java
// Avoid this:
try {
    // code
} catch (Exception e) {
    log.error("Operation failed.");
    e.printStackTrace(); // Redundant and can go to a different output stream
}

// Prefer this:
try {
    // code
} catch (Exception e) {
    log.error("Operation failed.", e); // Includes stack trace automatically
}
```

Following these practices makes logs more consistent, easier to search, and more valuable for debugging.