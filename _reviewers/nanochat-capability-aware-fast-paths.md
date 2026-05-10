---
title: Capability-Aware Fast Paths
description: 'When optimizing for speed, make the fast path both *correct for the
  actual hardware* and *lightweight in implementation*.


  1) Keep kernel support documentation accurate and capability-aware'
repository: karpathy/nanochat
label: Performance Optimization
language: Python
comments_count: 3
repository_stars: 53189
---

When optimizing for speed, make the fast path both *correct for the actual hardware* and *lightweight in implementation*.

1) Keep kernel support documentation accurate and capability-aware
- Maintain an explicit GPU architecture support matrix for optimized kernels.
- Only claim “Hopper-only” (or similar) if that’s true; otherwise document the actual compiled architectures.
- Ensure the code selects an appropriate fallback (e.g., SDPA) for unsupported architectures.

Example (pattern):
```python
# Supported FA3 archs reflect what kernels are compiled for
# sm90 (Hopper), sm89 (Ada), sm80/sm86 (Ampere)
# sm100 (Blackwell): fallback to SDPA until FA3 is recompiled

def _load_flash_attention_3():
    if not torch.cuda.is_available():
        return None
    # ... select FA3 vs fallback based on device capability ...
```

2) Avoid unnecessary overhead in parsing/utility code
- If checkpoint filenames are already guaranteed to match `model_<step>.pt`, prefer simple `split`/string ops over regex.
- Remove extra path manipulation (`basename`) when you already operate on plain filenames.

Example (pattern):
```python
# checkpoint_files contains only filenames like model_123456.pt
last_step = int(max(f.split("_")[-1].split(".")[0] for f in checkpoint_files))
```

Result: faster execution with fewer CPU-side bottlenecks, and fewer correctness surprises caused by stale/incorrect hardware assumptions.