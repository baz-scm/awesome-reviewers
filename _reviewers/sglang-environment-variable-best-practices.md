---
title: Environment variable best practices
description: Avoid reading environment variables directly in performance-critical
  code paths, especially during model forward passes or hot loops. Instead, read and
  cache environment variables during initialization or use dedicated helper functions
  for consistent handling.
repository: sgl-project/sglang
label: Configurations
language: Python
comments_count: 3
repository_stars: 17245
---

Avoid reading environment variables directly in performance-critical code paths, especially during model forward passes or hot loops. Instead, read and cache environment variables during initialization or use dedicated helper functions for consistent handling.

Use standardized helper functions like `get_bool_env_var()` instead of direct `os.getenv()` calls for better type safety and consistency. Follow clear naming conventions for environment variables, using descriptive prefixes like `SGLANG_` for project-specific settings.

Example of what to avoid:
```python
def forward_decode(self):
    # BAD: Reading env var in forward pass
    if os.getenv("USE_W4A8") != "1" and deep_gemm_wrapper.ENABLE_JIT_DEEPGEMM:
        # performance-critical code
```

Better approach:
```python
def __init__(self):
    # GOOD: Cache env var during initialization
    self.use_w4a8 = get_bool_env_var("SGLANG_USE_W4A8")
    
def forward_decode(self):
    # GOOD: Use cached value
    if not self.use_w4a8 and deep_gemm_wrapper.ENABLE_JIT_DEEPGEMM:
        # performance-critical code
```

This practice improves performance by avoiding repeated system calls and ensures consistent configuration handling across the codebase.