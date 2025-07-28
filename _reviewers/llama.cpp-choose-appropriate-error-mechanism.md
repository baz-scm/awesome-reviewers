---
title: Choose appropriate error mechanism
description: Use GGML_ASSERT for early validation and programming errors that indicate
  misconfigurations, but implement graceful error handling with logging for runtime
  conditions where fallback options exist. Assertions should catch problems early
  in development, while runtime errors should provide informative feedback and allow
  system recovery when possible.
repository: ggml-org/llama.cpp
label: Error Handling
language: C++
comments_count: 3
repository_stars: 83559
---

Use GGML_ASSERT for early validation and programming errors that indicate misconfigurations, but implement graceful error handling with logging for runtime conditions where fallback options exist. Assertions should catch problems early in development, while runtime errors should provide informative feedback and allow system recovery when possible.

For configuration validation and programming errors:
```cpp
// Good: Catch misconfiguration early
GGML_ASSERT(n_expert > 0 && "n_expert must be > 0 for SMALLTHINKER");
```

For runtime conditions with fallback options:
```cpp
// Good: Log and allow graceful fallback
if (!kernels) {
    GGML_LOG_DEBUG("%s: No suitable KleidiAI kernel available, falling back to standard CPU implementation\n", __func__);
    return false;  // Let the system fallback to standard CPU implementation
}
```

Avoid silent failures that provide no indication of what went wrong or that will cause assertions to fail later in the call chain. Always provide meaningful error messages or logging to aid debugging and system monitoring.