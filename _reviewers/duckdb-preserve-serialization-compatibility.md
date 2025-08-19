---
title: preserve serialization compatibility
description: When making changes to serialized data structures, always preserve backward
  and forward compatibility to prevent breaking existing databases and migration paths.
  This applies to enums, serialized plans, function serialization, and version handling.
repository: duckdb/duckdb
label: Migrations
language: Other
comments_count: 4
repository_stars: 32061
---

When making changes to serialized data structures, always preserve backward and forward compatibility to prevent breaking existing databases and migration paths. This applies to enums, serialized plans, function serialization, and version handling.

Key practices:
- **Append new enum values at the end** rather than reordering existing ones, as changing enum order breaks serialization
- **Avoid regenerating serialized plans** - if this becomes necessary, fix the underlying serialization issue instead
- **Use default values for new serialization fields** to maintain forward compatibility - fields with default values won't be serialized, allowing older versions to read newer serialized data
- **Use open-ended version ranges** (e.g., `v1.2.0+`) instead of closed ranges to accommodate ongoing compatibility

Example of safe enum extension:
```cpp
enum class CatalogType : uint8_t {
    INVALID = 0,
    TABLE_ENTRY = 1,
    SCHEMA_ENTRY = 2,
    // ... existing entries ...
    DATABASE_ENTRY = 9,
    NEW_ENTRY = 10,  // Append new entries at the end
};
```

Breaking serialization compatibility can render existing databases unreadable and disrupt migration workflows, making this a critical consideration for any schema or data structure changes.