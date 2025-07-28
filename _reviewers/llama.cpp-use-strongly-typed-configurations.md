---
title: Use strongly typed configurations
description: Prefer strongly typed configuration values over primitive types to improve
  code safety and clarity. Use enum classes instead of raw strings for categorical
  options, and proper boolean types instead of integer flags for binary settings.
repository: ggml-org/llama.cpp
label: Configurations
language: C++
comments_count: 2
repository_stars: 83559
---

Prefer strongly typed configuration values over primitive types to improve code safety and clarity. Use enum classes instead of raw strings for categorical options, and proper boolean types instead of integer flags for binary settings.

For categorical configurations, replace string parameters with enum classes:
```cpp
// Instead of:
params.dataset_format = format; // string

// Use:
enum class DatasetFormat { AUTO, TEXT, PARQUET, GGUF };
params.dataset_format = DatasetFormat::AUTO;
```

For boolean configurations, use explicit boolean conversion and values:
```cpp
// Instead of:
supports_set_rows = LLAMA_SET_ROWS ? atoi(LLAMA_SET_ROWS) : 0;

// Use:
supports_set_rows = LLAMA_SET_ROWS ? atoi(LLAMA_SET_ROWS) != 0 : false;
```

This approach prevents invalid configuration values, makes code more self-documenting, and enables better IDE support with auto-completion and type checking.