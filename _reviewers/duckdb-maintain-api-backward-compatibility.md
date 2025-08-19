---
title: maintain API backward compatibility
description: When evolving APIs, prioritize backward compatibility by creating new
  methods or overloads rather than modifying existing function signatures. This prevents
  breaking changes for existing users and extensions.
repository: duckdb/duckdb
label: API
language: Other
comments_count: 4
repository_stars: 32061
---

When evolving APIs, prioritize backward compatibility by creating new methods or overloads rather than modifying existing function signatures. This prevents breaking changes for existing users and extensions.

Key strategies include:
- Add new methods with descriptive names instead of changing existing ones (e.g., `duckdb_vector_slice_dictionary` instead of modifying `duckdb_slice_vector`)
- Provide overloaded versions when adding parameters (e.g., separate `FileHandle::Read` methods with and without `QueryContext`)
- Use proper memory management patterns in C APIs - allocate with `duckdb_malloc` so users can free with `duckdb_free`, or encapsulate complex data in opaque objects with accessor methods
- Avoid overly specialized helper functions that may become maintenance burdens; instead expose existing lower-level APIs that provide the same functionality

Example of good practice:
```cpp
// Instead of modifying existing signature:
// DUCKDB_C_API void duckdb_slice_vector(duckdb_vector vector, duckdb_selection_vector selection, idx_t len);

// Add a new method:
DUCKDB_C_API void duckdb_vector_slice_dictionary(duckdb_vector vector, idx_t dict_size, 
                                                  duckdb_selection_vector selection, idx_t len);
```

This approach ensures existing code continues to work while providing new functionality through clearly named, purpose-built interfaces.