---
title: Replace magic numbers
description: Replace magic numbers with named constants to improve code readability
  and maintainability. Magic numbers make code harder to understand and maintain,
  as their purpose and significance are not immediately clear to other developers.
repository: facebook/react-native
label: Code Style
language: Java
comments_count: 2
repository_stars: 123178
---

Replace magic numbers with named constants to improve code readability and maintainability. Magic numbers make code harder to understand and maintain, as their purpose and significance are not immediately clear to other developers.

When you encounter numeric literals in your code that have specific meaning or significance, extract them into well-named constants. This practice makes the code self-documenting and easier to modify in the future.

Example:
```java
// Instead of:
if (Math.abs(deltaX) > 1) {
    // handle scroll delta
}

// Use:
private static final int SCROLL_DELTA_EPSILON = 1;

if (Math.abs(deltaX) > SCROLL_DELTA_EPSILON) {
    // handle scroll delta
}
```

Additionally, avoid using arbitrary placeholder values that won't be used. If a value is not meaningful in certain contexts, consider using more explicit approaches like early returns with appropriate sentinel values rather than meaningless numbers.