---
title: Platform-Targeted Flags
description: When enabling/disabling CPU features or platform-specific APIs, derive
  decisions from the *configured target/platform* (toolchain/CMake target selection)
  and apply consistent compile-time guards across code and tests. Do not rely on compiler-defined
  feature macros that may differ between build/test environments.
repository: Tencent/ncnn
label: Configurations
language: Other
comments_count: 8
repository_stars: 23205
---

When enabling/disabling CPU features or platform-specific APIs, derive decisions from the *configured target/platform* (toolchain/CMake target selection) and apply consistent compile-time guards across code and tests. Do not rely on compiler-defined feature macros that may differ between build/test environments.

Apply it like this:
- In CMake/toolchains: explicitly set feature flags for the target (and force them in the toolchain when the target requires it).
  ```cmake
  # Toolchain for an older/limited target
  set(NCNN_AVX OFF  CACHE BOOL "Disable AVX"  FORCE)
  set(NCNN_AVX2 OFF CACHE BOOL "Disable AVX2" FORCE)
  set(NCNN_SSE2 ON  CACHE BOOL "Enable SSE2" FORCE)
  set(CMAKE_SYSTEM_VERSION 5.1)
  set(CMAKE_GENERATOR_PLATFORM "Win32")
  ```
- In headers/source: guard platform APIs/intrinsics with the correct target macros (prefer `_WIN32 && !(__MINGW32__)` over ad-hoc flags; keep intrinsics loads inside the matching arch block).
  ```c
  #if (defined _WIN32 && !(defined __MINGW32__))
  #define WIN32_LEAN_AND_MEAN
  #include <windows.h>
  #include <process.h>
  #endif

  #if __ARM_NEON
    float32x4_t _k0123 = vld1q_f32(kernel0);
  #else
    const float* k0 = kernel0;
  #endif
  ```
- In tests: determine capability based on the *target being executed* (x86/arm/Win32 target), not compiler macros like `__AVX__`.

This prevents “works in net.cpp, fails in ctest” and “breaks armv7 without NEON” class regressions, and keeps feature gating consistent across the build and runtime/test environments.