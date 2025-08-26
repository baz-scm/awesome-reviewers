---
title: Complete technical documentation
description: 'When documenting technical features, APIs, or data structures, provide
  comprehensive coverage that includes related functionality and detailed explanations
  rather than minimal inline comments. '
repository: tree-sitter/tree-sitter
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 21799
---

When documenting technical features, APIs, or data structures, provide comprehensive coverage that includes related functionality and detailed explanations rather than minimal inline comments. 

For complex technical concepts, prefer detailed prose explanations that can accommodate full context and examples. When documenting one feature, ensure related features are also covered to provide complete understanding.

For example, instead of:
```c
typedef struct {
  uint32_t row;    // zero-based
  uint32_t column; // zero-based, measured in bytes
```

Prefer comprehensive prose documentation:
```
In a point, rows and columns are zero-based. The `row` field represents the number of newlines before a given position, while `column` represents the number of bytes between the position and beginning of the line.
```

Similarly, when documenting predicates like `#any-eq?`, also document related predicates like `#any-not-eq?` to provide complete coverage of the feature set. This approach ensures developers have all necessary information in one place and reduces the need to search for related functionality elsewhere.