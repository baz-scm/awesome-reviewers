---
title: Verify operation semantics
description: 'When implementing algorithms that process collections or use conditional
  logic, always verify the exact semantics of operations across different data structures. '
repository: spring-projects/spring-framework
label: Algorithms
language: Other
comments_count: 2
repository_stars: 58382
---

When implementing algorithms that process collections or use conditional logic, always verify the exact semantics of operations across different data structures. 

For conditional operators like the Elvis operator (`?:`), be aware they may follow specific evaluation rules rather than intuitive reference semantics. For example, in SpEL, the Elvis operator checks for values that are non-null AND non-empty for Strings, which is more specific than general truthy/falsy rules from other languages:

```java
// This will inject 25 if pop3.port is null OR an empty string
@Value("${pop3.port ?: 25}")
private int port;
```

For operations that process collections, verify which data structures are actually supported. Selection operations in SpEL work not just on lists and maps, but also on arrays and anything implementing `java.lang.Iterable` or `java.util.Map` interfaces:

```java
// Works on lists, arrays, and any Iterable implementation
inventors.?[nationality == 'Serbian']
```

Understanding these semantics ensures your algorithms behave as expected across different data structures and prevents subtle bugs.