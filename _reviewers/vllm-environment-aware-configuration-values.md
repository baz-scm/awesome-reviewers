---
title: Environment-aware configuration values
description: When creating configuration files or defining configuration constants,
  ensure they properly adapt to different environments (Python versions, hardware
  architectures, etc.) with clear documentation. This prevents compatibility issues
  and helps other developers understand configuration choices.
repository: vllm-project/vllm
label: Configurations
language: Other
comments_count: 2
repository_stars: 51730
---

When creating configuration files or defining configuration constants, ensure they properly adapt to different environments (Python versions, hardware architectures, etc.) with clear documentation. This prevents compatibility issues and helps other developers understand configuration choices.

For dependency specifications:
- Use conditional dependencies with appropriate version constraints
- Document why constraints exist with specific references

```python
# Example: Properly constrained dependency with explanation
mistral_common[opencv] >= 1.6.2; python_version<="3.12" # Not compatible with Python 3.13 (see issue #XYZ)
```

For compile-time configuration constants:
- Use available detection mechanisms rather than hardcoding values
- Provide appropriate fallbacks with clear structure

```c++
// Example: Architecture-aware constant definition
#if defined(USE_ROCM)
  #if defined(__AMDGPU_WAVEFRONT_SIZE__)
    // Using compiler-provided macro for wavefront size
    #define WARP_SIZE __AMDGPU_WAVEFRONT_SIZE__
  #elif defined(__GFX9__)
    // Fallback for specific architecture
    #define WARP_SIZE 64
  #else
    // Default fallback
    #define WARP_SIZE 32
  #endif
#else // CUDA
  #define WARP_SIZE 32
#endif
```

Following these practices ensures configurations work correctly across diverse environments and remain maintainable as systems evolve.