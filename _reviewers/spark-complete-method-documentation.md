---
title: Complete method documentation
description: All public methods, especially in interfaces and APIs, must have comprehensive
  JavaDoc documentation that clearly describes their purpose, return values, and behavior.
  Avoid vague or ambiguous descriptions that leave developers guessing about the method's
  functionality.
repository: apache/spark
label: Documentation
language: Java
comments_count: 2
repository_stars: 41554
---

All public methods, especially in interfaces and APIs, must have comprehensive JavaDoc documentation that clearly describes their purpose, return values, and behavior. Avoid vague or ambiguous descriptions that leave developers guessing about the method's functionality.

Method documentation should be particularly thorough for public APIs since users may only have access to compiled JARs without source code comments. Each method should explicitly state what it returns, under what conditions, and any important behavioral details.

Example of unclear documentation:
```java
/**
 * Similar to {@link #toDDL()}, but returns the description of this constraint for describing
 */
```

Example of clear documentation:
```java
/**
 * Returns the constraint description for DESCRIBE TABLE output, excluding the constraint name (shown separately).
 */
```

For interface methods, always include JavaDoc even if the method signature seems self-explanatory, as this documentation becomes the primary reference for implementers and users of the API.