---
title: AI hardware platform support
description: AI applications must properly handle different GPU platforms (NVIDIA
  CUDA, AMD ROCm, Iluvatar Corex, etc.) through both build-time configuration and
  runtime capability detection. This ensures models can run efficiently across diverse
  hardware environments.
repository: comfyanonymous/ComfyUI
label: AI
language: Markdown
comments_count: 2
repository_stars: 83726
---

AI applications must properly handle different GPU platforms (NVIDIA CUDA, AMD ROCm, Iluvatar Corex, etc.) through both build-time configuration and runtime capability detection. This ensures models can run efficiently across diverse hardware environments.

Build-time considerations:
- Use parameterized builds to support different PyTorch variants for target platforms
- Configure appropriate package indices for platform-specific dependencies

Runtime considerations:
- Implement capability checks before using platform-specific features
- Provide graceful fallbacks when advanced features aren't supported
- Add platform detection logic to automatically adjust behavior

Example implementation:
```python
# Runtime capability check
def cuda_malloc_supported():
    # Check if platform supports cudaMallocAsync
    if platform_is_iluvatar():
        return False
    return True

# Build-time configuration
# docker build --build-arg VARIANT=cu126 .  # NVIDIA
# docker build --build-arg VARIANT=rocm6.2 .  # AMD
# python main.py --disable-cuda-malloc  # Iluvatar fallback
```

This approach ensures AI applications remain portable and performant across different hardware platforms while leveraging platform-specific optimizations when available.