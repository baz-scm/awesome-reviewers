---
title: Use descriptive names
description: Names should be descriptive and unambiguous, clearly communicating their
  purpose and intent. Avoid abbreviations and ambiguous terms that could confuse readers
  about the actual functionality or data being represented.
repository: duckdb/duckdb
label: Naming Conventions
language: Other
comments_count: 11
repository_stars: 32061
---

Names should be descriptive and unambiguous, clearly communicating their purpose and intent. Avoid abbreviations and ambiguous terms that could confuse readers about the actual functionality or data being represented.

Key principles:
- Expand abbreviated names for clarity (e.g., `additional_authenticated_data` instead of `aad`)
- Use semantic names that reflect actual purpose (e.g., `MISSING` instead of `INVALID` when data is absent, `HivePartitioningExecutor` instead of `HivePartitioning` for execution logic)
- Follow established naming conventions consistently (PascalCase for methods like `GetProgress()`, snake_case for variables like `ordinality_data`)
- Choose names that indicate data structure (e.g., `extension_directories` when storing multiple values)
- Use descriptive method names (e.g., `MicrosLength()` instead of generic `Length()`)

Example of good descriptive naming:
```cpp
// Bad: abbreviated and unclear
bool aad = false;
string extension_directory;
static idx_t Length(int32_t time[], char micro_buffer[]);

// Good: descriptive and clear
bool additional_authenticated_data = false;
vector<string> extension_directories;
static idx_t MicrosLength(int32_t micros, char micro_buffer[]);
```

Names should make code self-documenting and reduce the need for additional comments to understand functionality.