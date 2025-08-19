---
title: preserve existing environment variables
description: When modifying environment variables in code, always preserve existing
  values by appending or merging rather than overwriting. This prevents breaking existing
  configurations that may have been set by the system, other tools, or previous code
  execution.
repository: ClickHouse/ClickHouse
label: Configurations
language: Python
comments_count: 2
repository_stars: 42425
---

When modifying environment variables in code, always preserve existing values by appending or merging rather than overwriting. This prevents breaking existing configurations that may have been set by the system, other tools, or previous code execution.

Environment variables often contain multiple space-separated or colon-separated values that work together. Overwriting these variables can disable important functionality or cause unexpected behavior.

Example of the problem:
```python
# BAD: Overwrites existing TSAN_OPTIONS
env["TSAN_OPTIONS"] = f"memory_limit_mb={tsan_memory_limit_mb}"
```

Example of the correct approach:
```python
# GOOD: Preserves existing TSAN_OPTIONS and appends new values
tsan_options = f"memory_limit_mb={tsan_memory_limit_mb}"
env["TSAN_OPTIONS"] = env.get("TSAN_OPTIONS", "") + " " + tsan_options
```

This practice is especially important for debugging and profiling tools like TSAN, ASAN, and other environment-based configurations where multiple options need to coexist.