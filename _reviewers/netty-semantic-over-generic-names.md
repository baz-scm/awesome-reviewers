---
title: Semantic over generic names
description: Choose specific, descriptive names that clearly convey purpose over generic
  or abbreviated identifiers. Names should be self-documenting and unambiguous about
  their role.
repository: netty/netty
label: Naming Conventions
language: Java
comments_count: 9
repository_stars: 34227
---

Choose specific, descriptive names that clearly convey purpose over generic or abbreviated identifiers. Names should be self-documenting and unambiguous about their role.

Key guidelines:
- Replace generic terms with specific ones (e.g., 'type' → 'ordering')
- Avoid abbreviations unless universally understood
- Use complete words that describe the variable's purpose
- Ensure names reflect the actual functionality

Example:
```java
// Problematic - generic, unclear names
private int num;
private boolean type;
private String content;

// Better - specific, descriptive names
private int componentCount;
private boolean lastInFirstOutOrdering;
private String contentHeaderValue;
```

This practice improves code readability, reduces the need for additional documentation, and helps prevent misunderstandings during maintenance. When choosing names, consider whether another developer could understand the purpose without additional context.