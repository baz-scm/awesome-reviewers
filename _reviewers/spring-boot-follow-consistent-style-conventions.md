---
title: Follow consistent style conventions
description: 'Spring Boot projects maintain specific coding style conventions for
  consistency and readability. When contributing code, adhere to the following style
  guidelines:'
repository: spring-projects/spring-boot
label: Code Style
language: Java
comments_count: 8
repository_stars: 77637
---

Spring Boot projects maintain specific coding style conventions for consistency and readability. When contributing code, adhere to the following style guidelines:

1. **Explicit type declarations**: Don't use `var` keyword for variable declarations. Always declare variable types explicitly:
```java
// Incorrect:
var sessionStore = new MaxIdleTimeInMemoryWebSessionStore(timeout);

// Correct:
MaxIdleTimeInMemoryWebSessionStore sessionStore = new MaxIdleTimeInMemoryWebSessionStore(timeout);
```

2. **String comparison pattern**: Use "literal".equals(variable) pattern instead of Objects.equals():
```java
// Incorrect:
return Objects.equals(postgresAuthMethod, "trust");

// Correct:
return "trust".equals(postgresAuthMethod);
```

3. **Lambda expressions**: Use parentheses around single lambda parameters:
```java
// Incorrect:
.map(exporter -> BatchSpanProcessor.builder(exporter).build())

// Correct:
.map((exporter) -> BatchSpanProcessor.builder(exporter).build())
```

4. **Annotation consistency**: Explicitly declare annotations even when using default values for readability:
```java
// Keep annotations with default values for consistency
@Order(Ordered.LOWEST_PRECEDENCE)
```

5. **Regular expression syntax**: Be consistent with character escaping in regular expressions - if you escape opening brackets, also escape closing brackets:
```java
// Inconsistent:
Pattern.compile("^(.*)\\[(.*)\\]$");

// Consistent:
Pattern.compile("^(.*)\\[(.*)]$");
```

6. **Ordering**: Sort enum values and similar collections alphabetically for ease of finding items.

Following these conventions helps maintain a consistent codebase that's easier to read, review, and maintain.