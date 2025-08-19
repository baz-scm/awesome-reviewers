---
title: consistent null validation
description: Ensure null checks and input validation are applied consistently across
  similar functions and code paths. When one function in an API performs null pointer
  checks or input validation, all similar functions should follow the same pattern
  to maintain predictable behavior and prevent runtime errors.
repository: duckdb/duckdb
label: Null Handling
language: C++
comments_count: 5
repository_stars: 32061
---

Ensure null checks and input validation are applied consistently across similar functions and code paths. When one function in an API performs null pointer checks or input validation, all similar functions should follow the same pattern to maintain predictable behavior and prevent runtime errors.

Key practices:
- Add null pointer checks consistently across similar API functions
- Include input validation assertions (e.g., `D_ASSERT(!name.empty())`) for required parameters
- Validate data integrity (e.g., UTF8 validation for string types)
- Use comprehensive validation functions when available (e.g., `Value::IsFinite` instead of separate NaN and infinity checks)

Example from the codebase:
```cpp
// Before: Inconsistent null checking
char *duckdb_to_sql_string(duckdb_value val) {
    auto v = UnwrapValue(val);  // Missing null check
    // ...
}

// After: Consistent with other API functions
char *duckdb_to_sql_string(duckdb_value val) {
    if (!val) {
        return nullptr;  // Consistent null check like other functions
    }
    auto v = UnwrapValue(val);
    // ...
}
```

This pattern prevents inconsistent behavior where some functions handle null inputs gracefully while others crash, and ensures that validation logic is applied uniformly across the codebase.