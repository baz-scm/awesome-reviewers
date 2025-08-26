---
title: consolidate related logging
description: When logging information about the same operation or context, combine
  multiple related log statements into a single, comprehensive message rather than
  using separate log calls. This reduces log noise, improves readability, and can
  enhance performance by reducing the number of logging function calls.
repository: tree-sitter/tree-sitter
label: Logging
language: C
comments_count: 2
repository_stars: 21799
---

When logging information about the same operation or context, combine multiple related log statements into a single, comprehensive message rather than using separate log calls. This reduces log noise, improves readability, and can enhance performance by reducing the number of logging function calls.

Instead of multiple separate log statements:
```c
LOG("start_token chars:%lu", self->current_position.chars);
LOG("start_token row:%lu", self->current_point.row);
LOG("start_token column:%lu", self->current_point.column);
```

Consolidate into a single informative message:
```c
LOG("start_token chars:%lu, row:%lu, column:%lu", 
    self->current_position.chars, 
    self->current_point.row, 
    self->current_point.column);
```

Additionally, remove unnecessary or accidental logging parameters that don't provide value, as this simplifies logging macros and reduces maintenance overhead. Focus on logging only the information that is actually useful for debugging or monitoring purposes.