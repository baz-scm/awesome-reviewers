---
title: Extract for clarity
description: 'Extract complex or reused logic into focused, well-named methods with
  single responsibilities. This improves code readability, testability, and maintainability
  while reducing duplication. When refactoring:'
repository: elastic/elasticsearch
label: Code Style
language: Java
comments_count: 16
repository_stars: 73104
---

Extract complex or reused logic into focused, well-named methods with single responsibilities. This improves code readability, testability, and maintainability while reducing duplication. When refactoring:

1. Identify blocks of code that perform a distinct task or are used in multiple places
2. Extract them into appropriately named methods
3. Keep the scope of annotations like `@SuppressForbidden` minimal by extracting annotated code into dedicated helper methods
4. Consider creating separate classes for related logic sets

For example, instead of placing complex logic inline:

```java
@SuppressForbidden(
    reason = "TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993"
)
public static boolean parseBoolean(String value) {
    // complex implementation
    return Boolean.parseBoolean(value);
}
```

Extract it to minimize annotation scope:

```java
public static boolean parseBoolean(String value) {
    return parseBooleanInternal(value);
}

@SuppressForbidden(
    reason = "TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993"
)
private static boolean parseBooleanInternal(String value) {
    return Boolean.parseBoolean(value);
}
```

For complex class functionality, consider isolating related methods:

```java
// Comment from Discussion 6: 
// "A logistical suggestion would be to isolate all the InlineJoin logic into its own class 
// (could be nested), as there are a few methods here (plus this record) 
// that are dedicated just for this feature."
```

This approach makes code more maintainable, easier to understand, and simplifies future changes.
