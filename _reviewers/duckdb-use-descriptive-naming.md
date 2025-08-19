---
title: Use descriptive naming
description: Choose names that clearly communicate intent and purpose rather than
  being generic, abbreviated, or potentially misleading. Names should accurately reflect
  what the code does, not how it does it.
repository: duckdb/duckdb
label: Naming Conventions
language: C++
comments_count: 11
repository_stars: 32061
---

Choose names that clearly communicate intent and purpose rather than being generic, abbreviated, or potentially misleading. Names should accurately reflect what the code does, not how it does it.

Key principles:
- Use domain-specific terminology (`column_idx` instead of `field_idx` for database operations)
- Choose method names that describe the action (`SerializeToDisk` instead of `GetStorageInfo`, `LogFailure` instead of `LogBoth`)
- Make boolean flags readable (`supports_ordinality` instead of `ordinality_implemented`)
- Spell out full names instead of abbreviations (`"replace"` instead of `"r"` for error handling modes)
- Use named constants instead of magic numbers (`match_actions.size()` instead of hardcoded `3`)
- Avoid names that contradict behavior (don't name something `extension_loading = none` when it actually loads extensions)

Example:
```cpp
// Avoid generic or misleading names
void GetStorageInfo(optional_ptr<ClientContext> context, bool all_expr_inputs_valid);
for (idx_t match_idx = 0; match_idx < 3; match_idx++) { // magic number

// Use descriptive, intent-revealing names  
void SerializeToDisk(optional_ptr<ClientContext> context, bool all_inputs_valid);
for (idx_t match_idx = 0; match_idx < match_actions.size(); match_idx++) { // named constant
```

This approach makes code self-documenting and reduces the cognitive load for developers reading and maintaining the codebase.