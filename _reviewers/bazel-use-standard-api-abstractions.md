---
title: Use standard API abstractions
description: Prefer established, type-safe abstractions over primitive types or direct
  property access when designing APIs. This improves maintainability, enables future
  extensibility, and provides better developer experience.
repository: bazelbuild/bazel
label: API
language: Other
comments_count: 3
repository_stars: 24489
---

Prefer established, type-safe abstractions over primitive types or direct property access when designing APIs. This improves maintainability, enables future extensibility, and provides better developer experience.

Use standard library types and framework-provided abstractions instead of custom primitives:
- Use `google.protobuf.Duration` instead of `int64` millisecond fields
- Use `std::string_view` instead of `const char*` for string parameters
- Use framework argument builders instead of direct property access like `.path`

Example improvements:
```cpp
// Instead of:
static bool IsValidEnvName(const char* p) { ... }

// Use:
static bool IsValidEnvName(std::string_view name) { ... }
```

```proto
// Instead of:
int64 critical_path_time_in_ms = 4;

// Use:
google.protobuf.Duration critical_path_time = 4;
```

These abstractions often provide additional functionality (like automatic path mapping, timezone handling, or memory efficiency) and make APIs more robust and future-proof.