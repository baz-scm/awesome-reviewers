---
title: Guard expensive logging operations
description: Avoid executing expensive operations in logging code paths when logging
  is disabled or not needed. Always check if logging should occur before performing
  costly operations like string construction, formatting, or data processing for log
  messages.
repository: duckdb/duckdb
label: Logging
language: C++
comments_count: 3
repository_stars: 32061
---

Avoid executing expensive operations in logging code paths when logging is disabled or not needed. Always check if logging should occur before performing costly operations like string construction, formatting, or data processing for log messages.

The key principle is to separate the lightweight "should log" check from expensive log message preparation. This prevents performance overhead when logging is disabled and avoids unnecessary work like duplicate string construction or complex data processing.

Example of the problem:
{% raw %}
```cpp
// BAD: Always executes expensive operation
const auto event = state.offset_in_group == (idx_t)group.num_rows ? "SkipRowGroup" : "ReadRowGroup";
DUCKDB_LOG(context, PhysicalOperatorLogType, *state.op, "ParquetReader", event,
           {{"file", file.path}, {"row_group_id", to_string(state.group_idx_list[state.current_group])}});
```
{% endraw %}

Better approach:
```cpp
// GOOD: Guard expensive operations behind logging check
if (DUCKDB_SHOULD_LOG(context, PhysicalOperatorLogType)) {
    const auto event = state.offset_in_group == (idx_t)group.num_rows ? "SkipRowGroup" : "ReadRowGroup";
    vector<pair<string, string>> log_payload = {
        {"file", file.path},
        {"row_group_id", to_string(state.group_idx_list[state.current_group])}
    };
    DUCKDB_WRITE_LOG(context, PhysicalOperatorLogType, *state.op, "ParquetReader", event, log_payload);
}
```

This pattern is especially important for high-frequency logging in performance-critical code paths, and helps avoid creating log messages multiple times for different output streams.