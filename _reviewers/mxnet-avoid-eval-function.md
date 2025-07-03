---
title: Avoid eval function
description: Never use the `eval()` function in Python code as it creates serious
  security vulnerabilities by executing arbitrary code at runtime. This can lead to
  code injection attacks when processing user inputs or data from untrusted sources.
repository: apache/mxnet
label: Security
language: Python
comments_count: 1
repository_stars: 20801
---

Never use the `eval()` function in Python code as it creates serious security vulnerabilities by executing arbitrary code at runtime. This can lead to code injection attacks when processing user inputs or data from untrusted sources.

Instead of using `eval()` to convert strings to booleans or other types, use explicit type conversion or conditional logic:

```python
# INSECURE - vulnerable to code injection:
def setting_ctx(use_gpu):
    if eval(use_gpu):
        # code that uses GPU
        
# SECURE - using explicit boolean conversion:
def setting_ctx(use_gpu):
    if isinstance(use_gpu, str):
        use_gpu = use_gpu.lower() in ('true', 'yes', '1', 'y')
    if use_gpu:
        # code that uses GPU
```

For other type conversions, use appropriate functions like `int()`, `float()`, or `json.loads()` to safely parse data without executing code.
