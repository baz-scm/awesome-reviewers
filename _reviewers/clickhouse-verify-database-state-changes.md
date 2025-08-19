---
title: Verify database state changes
description: When testing database operations that modify schema, data, or metadata,
  always add comprehensive assertions to verify the expected state changes. Database
  operations often have side effects beyond the primary action, and tests should validate
  both the intended outcome and related system state.
repository: ClickHouse/ClickHouse
label: Database
language: Python
comments_count: 3
repository_stars: 42425
---

When testing database operations that modify schema, data, or metadata, always add comprehensive assertions to verify the expected state changes. Database operations often have side effects beyond the primary action, and tests should validate both the intended outcome and related system state.

Key verification patterns:
- **Schema changes**: After ALTER operations, verify the new schema with `SHOW CREATE TABLE` or similar introspection queries
- **Data operations**: After DROP/DELETE operations, explicitly check data persistence or removal as intended
- **Metadata cleanup**: After replica/node removal operations, verify that associated metadata (like ZooKeeper nodes) are properly cleaned up

Example from schema evolution test:
```python
# After schema modification
instance.query(f"ALTER TABLE {TABLE_NAME} MODIFY COLUMN x Int64;")
# Verify the schema change took effect
result = instance.query(f"SHOW CREATE TABLE {TABLE_NAME}")
assert "Int64" in result
```

Example from drop operations:
```python
# After dropping table/replica
drop_iceberg_table(instance, TABLE_NAME)
# Verify data still exists if that's the expected behavior
files = get_table_files(TABLE_NAME)
assert len(files) > 0, "Drop should not delete user data"
```

This approach catches subtle bugs where operations appear to succeed but don't have the expected side effects, ensuring database tests provide comprehensive coverage of system behavior.