---
title: explicit performance handling
description: When writing performance benchmarking and measurement code, always be
  explicit about all possible cases and organize related constants clearly. Avoid
  catch-all else clauses that could mask bugs or unexpected values in performance-critical
  code paths.
repository: ggml-org/llama.cpp
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 83559
---

When writing performance benchmarking and measurement code, always be explicit about all possible cases and organize related constants clearly. Avoid catch-all else clauses that could mask bugs or unexpected values in performance-critical code paths.

This approach prevents silent failures in benchmark parsing and makes performance code more maintainable by clearly documenting all expected scenarios.

Example of explicit case handling:
```python
# Instead of a catch-all else clause
if unit == "TFLOPS":
    gflops = value * 1000
elif unit == "MFLOPS":
    gflops = value / 1000
elif unit == "GFLOPS":
    gflops = value
else:
    assert False  # Explicit failure for unexpected units
```

Example of organized performance constants:
```python
# Clearly separate constants by benchmark type
LLAMA_BENCH_BOOL_PROPERTIES = ["embeddings", "cpu_strict", "use_mmap", "no_kv_offload", "flash_attn"]
TEST_BACKEND_OPS_BOOL_PROPERTIES = ["supported", "passed"]
```