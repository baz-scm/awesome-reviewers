---
title: Stable schema identifiers
description: Use persistent identifiers for schema elements rather than relying on
  positional information or enumeration, which can break when schema changes occur.
  Assign unique, immutable IDs to database objects like tables and columns, and ensure
  these IDs remain stable throughout the object's lifecycle.
repository: influxdata/influxdb
label: Database
language: Rust
comments_count: 5
repository_stars: 30268
---

Use persistent identifiers for schema elements rather than relying on positional information or enumeration, which can break when schema changes occur. Assign unique, immutable IDs to database objects like tables and columns, and ensure these IDs remain stable throughout the object's lifecycle.

For example, instead of:
```rust
// Problematic - using enumeration for column IDs
.enumerate()
.map(|(idx, (col_type, f))| {
    // Using idx as column ID is dangerous
    ColumnDefinition::new(idx, f.name(), col_type, f.is_nullable())
})
```

Use a system that generates and persists stable IDs:
```rust
// Better - using dedicated ID generation
let column_id = table_def.next_column_id();
ColumnDefinition::new(column_id, f.name(), col_type, f.is_nullable())
```

When designing schema access patterns, minimize catalog locks by including ID-to-name mappings in cached schema objects. Use IDs for internal lookups and operations for performance, while preserving names for user-facing interfaces. When serializing schema objects, ensure both IDs and names are properly preserved to maintain the mapping integrity.

During schema changes like adding columns, preserve existing IDs and assign new IDs to new elements, rather than reassigning all IDs. This guarantees that references to existing columns remain valid even as the schema evolves.