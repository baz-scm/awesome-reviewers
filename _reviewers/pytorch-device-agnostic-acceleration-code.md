---
title: Device-agnostic acceleration code
description: Avoid hardcoding specific device types like 'cuda' in AI code. Instead,
  use device-agnostic approaches such as device type variables or accelerator detection
  functions. This ensures code runs efficiently across different hardware accelerators
  (CUDA, ROCm, XPU, etc.) without modification.
repository: pytorch/pytorch
label: AI
language: Python
comments_count: 11
repository_stars: 91345
---

Avoid hardcoding specific device types like 'cuda' in AI code. Instead, use device-agnostic approaches such as device type variables or accelerator detection functions. This ensures code runs efficiently across different hardware accelerators (CUDA, ROCm, XPU, etc.) without modification.

Examples:
```python
# Instead of this:
x = torch.randn(100, 100, device='cuda')

# Do this:
x = torch.randn(100, 100, device=GPU_TYPE)

# Or for more dynamic detection:
device = torch.accelerator.current_accelerator().type if torch.accelerator.current_accelerator() else "cpu"
x = torch.randn(100, 100, device=device)
```

This approach helps maintain compatibility with various AI hardware acceleration platforms and simplifies testing across multiple device types. For common test cases, prefer using constants like `GPU_TYPE` defined in testing utilities, and for production code, use the accelerator API to detect available devices at runtime.