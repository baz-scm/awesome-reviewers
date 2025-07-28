---
title: consistent null handling
description: Maintain consistency in null handling patterns across the codebase. When
  multiple approaches exist for representing absent or disabled values, choose one
  approach and apply it uniformly throughout the project.
repository: apache/spark
label: Null Handling
language: Java
comments_count: 2
repository_stars: 41554
---

Maintain consistency in null handling patterns across the codebase. When multiple approaches exist for representing absent or disabled values, choose one approach and apply it uniformly throughout the project.

Common inconsistencies to avoid:
- Mixing sentinel values (like -1) with Optional types - prefer Optional types for better null safety
- Mixing null checks with length/isEmpty checks - prefer length/isEmpty for collections and arrays

Example of improving consistency:
```java
// Instead of mixing approaches:
private long numTargetRowsCopied = -1;  // sentinel value
if (rowBasedChecksums != null) { ... }  // null check

// Use consistent patterns:
private OptionalLong numTargetRowsCopied = OptionalLong.empty();  // Optional type
if (rowBasedChecksums.length > 0) { ... }  // length check
```

This consistency improves code readability, reduces cognitive load for developers, and prevents bugs that arise from mixing different null handling strategies in the same codebase.