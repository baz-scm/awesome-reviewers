---
title: Platform-specific configuration guards
description: 'When implementing platform-specific or version-dependent code, use the
  simplest and most maintainable configuration guards. Follow these practices:


  1. **Use the simplest sufficient guard:** If a feature is already gated to a specific
  platform by a build flag, avoid adding redundant architecture checks.'
repository: pytorch/pytorch
label: Configurations
language: Other
comments_count: 5
repository_stars: 91169
---

When implementing platform-specific or version-dependent code, use the simplest and most maintainable configuration guards. Follow these practices:

1. **Use the simplest sufficient guard:** If a feature is already gated to a specific platform by a build flag, avoid adding redundant architecture checks.
   ```cpp
   // Prefer this (if USE_FBGEMM is already x86-specific)
   #ifdef USE_FBGEMM
   // FBGEMM-specific code
   #endif
   
   // Instead of this
   #if defined(USE_FBGEMM) && (defined(__x86_64__) || defined(_M_X64))
   // FBGEMM-specific code
   #endif
   ```

2. **Create helper macros for version checks:** For recurring version-dependent features, define clear helper macros to improve readability.
   ```cpp
   // Define a reusable macro for CUDA version checks
   #if defined(CUDA_VERSION) && CUDA_VERSION >= 12030
   #define IF_CUDA_VERSION_GE_12030(x) x
   #else
   #define IF_CUDA_VERSION_GE_12030(x)
   #endif
   ```

3. **Consider API consistency:** When conditional compilation affects public APIs, prefer implementing the API unconditionally but throwing runtime errors for unavailable features rather than completely omitting the API.
   ```cpp
   // Prefer this (consistent API, runtime check)
   void initVulkanModule(PyObject* module) {
   #ifdef USE_VULKAN
     // Actual implementation
   #else
     throw std::runtime_error("Vulkan support not available");
   #endif
   }
   
   // Instead of conditionally defining the function entirely
   ```

Following these practices ensures your code is more maintainable, provides consistent APIs across different builds, and avoids unnecessary complexity in platform-specific sections.
