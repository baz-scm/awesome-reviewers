---
title: thoughtful configuration design
description: When designing configuration options, environment variables, and build
  settings, follow established patterns and ensure they serve a clear purpose. Consider
  cross-platform compatibility, use familiar conventions (like PATH-style lists),
  and align configuration choices with project requirements.
repository: duckdb/duckdb
label: Configurations
language: Txt
comments_count: 3
repository_stars: 32061
---

When designing configuration options, environment variables, and build settings, follow established patterns and ensure they serve a clear purpose. Consider cross-platform compatibility, use familiar conventions (like PATH-style lists), and align configuration choices with project requirements.

Key principles:
- Follow established patterns (e.g., colon/semicolon-separated lists like PATH)
- Handle platform differences appropriately (`;` on Windows, `:` on Unix)
- Ensure every configuration variable is actually used - avoid creating intermediate variables that serve no purpose
- Align configuration granularity with project compatibility guarantees (e.g., version numbering should reflect actual compatibility boundaries)
- Remove unused configuration variables rather than leaving them as dead code

Example:
```cmake
# Good: Uses platform-appropriate separators and follows PATH convention
set(EXTENSION_DIRECTORIES "~/.duckdb/extensions" CACHE STRING "Extension directories (colon/semicolon separated)")

# Good: Version reflects actual compatibility guarantees  
set_target_properties(duckdb PROPERTIES SOVERSION ${DUCKDB_MAJOR_VERSION}.${DUCKDB_MINOR_VERSION})

# Bad: Creates unused intermediate variable
set(SUMMARIZE_FAILURES_ENV "$ENV{SUMMARIZE_FAILURES}")  # Never actually used
```