---
title: ensure test cleanup
description: Tests must properly clean up resources and handle conditional execution
  regardless of test outcome. This includes removing temporary files, resetting global
  state, and gracefully handling feature flag conditions.
repository: cloudflare/workerd
label: Testing
language: Other
comments_count: 2
repository_stars: 6989
---

Tests must properly clean up resources and handle conditional execution regardless of test outcome. This includes removing temporary files, resetting global state, and gracefully handling feature flag conditions.

For file-based tests, use RAII patterns or explicit cleanup in finally blocks to ensure resources are released even when tests fail:

```cpp
KJ_TEST("PerfettoSession basic functionality") {
  auto traceFile = getTempFileName("perfetto-test");
  
  // Use RAII or try-finally pattern
  KJ_DEFER(removeFile(traceFile.cStr()));
  
  {
    PerfettoSession session(traceFile, "workerd");
    // ... test operations
  }
  
  KJ_ASSERT(fileExists(traceFile.cStr()));
  // File automatically cleaned up by KJ_DEFER
}
```

For tests that depend on feature flags or autogates, check conditions early and skip gracefully rather than creating complex conditional logic:

```cpp
KJ_TEST("feature dependent test") {
  if (util::Autogate::isEnabled("feature-flag")) {
    KJ_LOG(INFO, "Skipping test due to autogate being enabled");
    return;
  }
  
  // ... rest of test
}
```

This prevents resource leaks, reduces flaky tests, and makes test behavior predictable across different environments and configurations.