---
title: Prefer Optional over nulls
description: 'Use Java''s Optional API instead of null checks to improve code readability,
  safety, and maintainability. When dealing with potentially absent values:

  '
repository: quarkusio/quarkus
label: Null Handling
language: Java
comments_count: 5
repository_stars: 14667
---

Use Java's Optional API instead of null checks to improve code readability, safety, and maintainability. When dealing with potentially absent values:

1. Return Optional<T> instead of T that might be null
2. Use Optional's functional methods (ifPresent, map, flatMap, orElse) rather than null checks
3. Avoid Optional.get() without first checking isPresent()
4. When comparing values that might be null, use Objects.equals() or place potentially null values on the right side of equals comparisons

Example:
```java
// Not recommended
String principalClaim = resolvedContext.oidcConfig().token().principalClaim().orElse(null);
if (principalClaim != null && !tokenJson.containsKey(principalClaim)) {
    // do something with principalClaim
}

// Recommended
resolvedContext.oidcConfig().token().principalClaim().ifPresent(claim -> {
    if (!tokenJson.containsKey(claim)) {
        // do something with claim
    }
});
```

For performance-critical code paths, consider using specialized patterns like returning pre-defined constants (e.g., Collections.emptyMap()) instead of allocating new objects when a value is absent.