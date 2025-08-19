---
title: prefer settings over pragmas
description: When implementing configuration options, prefer database settings over
  pragma functions to maintain consistency and better user experience. Settings provide
  a unified interface that's easier to discover, document, and manage compared to
  scattered pragma functions.
repository: duckdb/duckdb
label: Configurations
language: C++
comments_count: 4
repository_stars: 32061
---

When implementing configuration options, prefer database settings over pragma functions to maintain consistency and better user experience. Settings provide a unified interface that's easier to discover, document, and manage compared to scattered pragma functions.

Instead of creating pragma functions like:
```cpp
set.AddFunction(PragmaFunction::PragmaStatement("enable_logging", PragmaEnableLogging));
```

Use database settings:
```cpp
// In settings registration
void EnableLoggingSetting::SetGlobal(DatabaseInstance *db, DBConfig &config, const Value &input) {
    config.options.enable_logging = input.GetValue<bool>();
}
```

This approach consolidates configuration management, eliminates the need for environment variables scattered throughout the codebase, and provides a consistent `SET variable=value` interface. When multiple configuration sources exist (environment variables, pragma functions, attach options), refactor them into a unified settings system to reduce complexity and potential conflicts. Consider using table functions (`CALL enable_logging(...)`) for operations that require parameters or complex logic, but keep simple boolean/value configurations as settings.