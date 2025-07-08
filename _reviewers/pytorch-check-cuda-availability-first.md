---
title: Check CUDA availability first
description: 'Always verify CUDA availability before performing CUDA-specific operations
  to prevent runtime errors when code runs on systems without CUDA support. When working
  with device-specific code:'
repository: pytorch/pytorch
label: Pytorch
language: Python
comments_count: 3
repository_stars: 91345
---

Always verify CUDA availability before performing CUDA-specific operations to prevent runtime errors when code runs on systems without CUDA support. When working with device-specific code:

1. Add explicit checks with `torch.cuda.is_available()` before any CUDA-specific operations
2. Use appropriate device properties rather than just device names for better cross-platform compatibility
3. Handle device-like parameters consistently using proper abstractions

Example:
```python
# Bad - may fail on CPU-only systems
if torch.cuda.is_current_stream_capturing():
    # CUDA-specific code

# Good - safely checks CUDA availability first
if torch.cuda.is_available() and torch.cuda.is_current_stream_capturing():
    # CUDA-specific code

# Better device property handling - use specific properties instead of just names
device = input_nodes[0].get_device()
if device.type == "cuda":
    # Use specific device properties for hardware identification
    device_properties = torch.cuda.get_device_properties(device.index)
    # Use properties like device_properties.major, device_properties.minor, etc.
```

This approach ensures code works reliably across different hardware configurations and gracefully handles CPU-only environments.