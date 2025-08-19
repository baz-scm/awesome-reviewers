---
title: maintain codebase consistency
description: Ensure new code follows established patterns, conventions, and standards
  already present in the codebase. This includes adhering to parameter ordering conventions,
  maintaining existing code patterns, using consistent header formatting, and reusing
  existing utilities rather than creating duplicates.
repository: duckdb/duckdb
label: Code Style
language: Other
comments_count: 6
repository_stars: 32061
---

Ensure new code follows established patterns, conventions, and standards already present in the codebase. This includes adhering to parameter ordering conventions, maintaining existing code patterns, using consistent header formatting, and reusing existing utilities rather than creating duplicates.

Key areas to check:
- **Parameter ordering**: Follow established conventions for parameter order (e.g., allocators as first parameters)
- **Code patterns**: Maintain existing patterns rather than introducing new approaches without justification
- **Header formatting**: Use consistent header comment blocks across all files
- **Constructor design**: Avoid unnecessary constructors when implicit conversions or default values suffice
- **Code reuse**: Leverage existing utility functions instead of reimplementing similar functionality

Example of good consistency:
```cpp
// Follow established parameter ordering
string_t(ArenaAllocator &arena, const char *data, const uint32_t len) // Good
string_t(const char *data, const uint32_t len, ArenaAllocator &arena) // Inconsistent

// Use standard header format
//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/types/string.hpp
//
//===----------------------------------------------------------------------===//
```

This approach reduces cognitive load for developers, makes the codebase more predictable, and prevents the accumulation of inconsistent patterns over time.