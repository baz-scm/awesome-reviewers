---
title: Use accelerator-agnostic code
description: Write code that works across different hardware accelerators by using
  PyTorch's accelerator abstraction API rather than hardcoding device-specific logic.
  This prevents failures when code runs on different hardware platforms like CPU,
  CUDA, ROCm, or other accelerators.
repository: pytorch/pytorch
label: Pytorch
language: Python
comments_count: 12
repository_stars: 91169
---

Write code that works across different hardware accelerators by using PyTorch's accelerator abstraction API rather than hardcoding device-specific logic. This prevents failures when code runs on different hardware platforms like CPU, CUDA, ROCm, or other accelerators.

Instead of checking for specific device types or hardcoding device names:

```python
# Problematic: Device-specific code
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
tensor = torch.randn(3, 3).cuda()  # Fails on non-CUDA systems
```

Use the accelerator API for device detection and management:

```python
# Better: Accelerator-agnostic code
device = (torch.accelerator.current_accelerator().type 
          if torch.accelerator.is_available() 
          else "cpu")
tensor = torch.randn(3, 3).to(device)  # Works on any system
```

When writing tests, avoid assuming specific devices:

```python
# Instead of:
@requires_cuda
def test_feature():
    x = torch.randn(3, 3).cuda()
    # test code

# Do this:
@requires_accelerator
def test_feature():
    device = torch.accelerator.current_accelerator().type
    x = torch.randn(3, 3).to(device)
    # test code
```

By writing accelerator-agnostic code, you ensure your PyTorch code works consistently across different hardware platforms without modification.
