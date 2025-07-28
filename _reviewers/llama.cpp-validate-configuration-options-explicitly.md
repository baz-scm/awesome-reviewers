---
title: validate configuration options explicitly
description: When handling configuration options or tool types, use explicit conditional
  statements with proper error handling for unknown values instead of implicit fallbacks
  or else clauses. This prevents silent failures and makes it clear which configurations
  are supported.
repository: ggml-org/llama.cpp
label: Configurations
language: Python
comments_count: 3
repository_stars: 83559
---

When handling configuration options or tool types, use explicit conditional statements with proper error handling for unknown values instead of implicit fallbacks or else clauses. This prevents silent failures and makes it clear which configurations are supported.

Use `elif` statements for each known configuration option and include an `assert False` or explicit error for unhandled cases:

```python
if self.tool == "llama-bench":
    self.check_keys = set(LLAMA_BENCH_KEY_PROPERTIES + ["build_commit", "test_time", "avg_ts"])
elif self.tool == "test-backend-ops":
    self.check_keys = set(TEST_BACKEND_OPS_KEY_PROPERTIES + ["build_commit", "test_time"])
else:
    assert False, f"Unknown tool type: {self.tool}"
```

This approach helps catch configuration errors early, makes the supported options explicit in the code, and prevents issues like duplicate settings or silent overwrites that can occur with implicit handling. When adding new configuration options, developers must explicitly update the validation logic, ensuring all cases are properly considered.