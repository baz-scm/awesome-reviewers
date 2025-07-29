---
title: prefer modern collection APIs
description: 'Use modern collection creation methods instead of legacy alternatives
  for improved readability and conciseness. Replace older patterns with their modern
  equivalents:'
repository: apache/kafka
label: Code Style
language: Java
comments_count: 8
repository_stars: 30575
---

Use modern collection creation methods instead of legacy alternatives for improved readability and conciseness. Replace older patterns with their modern equivalents:

- Use `List.of()` instead of `Arrays.asList()` or `Collections.singletonList()`
- Use `Set.of()` instead of `new HashSet<>(Arrays.asList(...))`
- Use `.toList()` instead of `.collect(Collectors.toList())`
- Use `Collections.emptyList()` → `List.of()` when creating empty immutable lists

Example transformations:
```java
// Before
List<String> items = Arrays.asList("a", "b", "c");
Set<String> permissions = new HashSet<>(Arrays.asList("READ", "WRITE"));
List<String> results = stream.collect(Collectors.toList());

// After  
List<String> items = List.of("a", "b", "c");
Set<String> permissions = Set.of("READ", "WRITE");
List<String> results = stream.toList();
```

Modern collection APIs are more concise, expressive, and create immutable collections by default, which helps prevent accidental modifications and improves code safety. They also eliminate the need for intermediate collection creation steps, making the code more direct and readable.