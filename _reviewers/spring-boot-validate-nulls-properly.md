---
title: Validate nulls properly
description: 'Always use appropriate null validation mechanisms to prevent NullPointerExceptions
  and ensure code robustness.


  For string parameters:

  - Use `Assert.hasText(profile, "Profile must have text")` instead of `Assert.notNull()`
  when you need to validate both null and empty strings'
repository: spring-projects/spring-boot
label: Null Handling
language: Java
comments_count: 3
repository_stars: 77637
---

Always use appropriate null validation mechanisms to prevent NullPointerExceptions and ensure code robustness.

For string parameters:
- Use `Assert.hasText(profile, "Profile must have text")` instead of `Assert.notNull()` when you need to validate both null and empty strings
- This handles both null checks and empty string validation in one call

For equals methods:
- Always check for null before comparing class types:
```java
@Override
public boolean equals(Object obj) {
    if (this == obj) {
        return true;
    }
    if (obj == null || getClass() != obj.getClass()) {
        return false;
    }
    // Continue with comparison
}
```

For collections and arrays:
- Always validate that collection parameters are not null before processing them
- For optional collections, consider:
```java
if (resolvers != null) {
    // process resolvers
}
```
- Or enforce non-null values through constructor validation

Using these patterns consistently will reduce null-related bugs and improve code quality across the codebase.