---
title: Use descriptive semantic names
description: Names should accurately reflect their purpose, behavior, and semantic
  meaning to avoid confusion and improve code readability. Avoid misleading names
  that don't match the actual functionality or content.
repository: ClickHouse/ClickHouse
label: Naming Conventions
language: C++
comments_count: 11
repository_stars: 42425
---

Names should accurately reflect their purpose, behavior, and semantic meaning to avoid confusion and improve code readability. Avoid misleading names that don't match the actual functionality or content.

Key principles:
- Function names should match their actual behavior (e.g., `projectCorrelatedColumns` when called with non-correlated data should be renamed to reflect what it actually does)
- Variable names should be specific and unambiguous (e.g., `cached_reader` is misleading when it specifically refers to `CachedInMemoryReadBufferFromFile` - use `page_cache_reader` instead)
- Parameter names should clearly indicate their role (e.g., `column_idx` should be `presence_column_idx` if it's specifically the index of a presence column)
- Avoid abbreviations that sacrifice clarity (e.g., use `storage` or `table` instead of `tbl`)
- Method names should indicate what they return or do (e.g., `getHivePart()` should be split into separate methods if it also performs normalization)

Example of improvement:
```cpp
// Before: misleading name
void projectCorrelatedColumns(rhs_plan, ...);  // but no correlation involved

// After: accurate name  
void projectIdentifierColumns(rhs_plan, ...);  // clearly indicates projecting from identifiers

// Before: ambiguous variable
auto * cached_reader = typeid_cast<CachedInMemoryReadBufferFromFile *>(&reader);

// After: specific variable
auto * page_cache_reader = typeid_cast<CachedInMemoryReadBufferFromFile *>(&reader);
```

This ensures that code is self-documenting and reduces cognitive load when reading and maintaining the codebase.