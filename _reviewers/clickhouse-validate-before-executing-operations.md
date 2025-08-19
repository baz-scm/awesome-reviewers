---
title: validate before executing operations
description: Always validate inputs and preconditions before executing database operations,
  and fail explicitly rather than silently ignoring invalid states or configurations.
  This prevents data corruption, ensures system consistency, and makes debugging easier.
repository: ClickHouse/ClickHouse
label: Database
language: C++
comments_count: 8
repository_stars: 42425
---

Always validate inputs and preconditions before executing database operations, and fail explicitly rather than silently ignoring invalid states or configurations. This prevents data corruption, ensures system consistency, and makes debugging easier.

Key validation practices:
- Check existence of required resources before operations (e.g., replicas, tables, columns)
- Validate configuration compatibility (e.g., partition strategies with data lakes)
- Throw explicit errors for invalid inputs rather than silently ignoring them
- Verify schema consistency before schema changes
- Ensure backward compatibility when making breaking changes

Example from the discussions:
```cpp
// Bad: Silently ignore column list
if (open_bracket.ignore(pos, expected))
{
    // Column list parsing but then ignored
}

// Good: Validate and throw if invalid
if (open_bracket.ignore(pos, expected))
{
    throw Exception(ErrorCodes::BAD_ARGUMENTS, 
        "Column list specification is not supported in this context");
}

// Good: Check existence before operations  
if (!zookeeper->exists(zookeeper_path + "/replicas/" + replica_name))
{
    // Skip operation as replica doesn't exist
    return;
}
```

This approach prevents silent failures, makes systems more predictable, and helps maintain data integrity across complex database operations.