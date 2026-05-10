---
title: Conditional CMake Configuration
description: When changing build configuration (compiler definitions, link libraries,
  compile/link flags), ensure it is applied only when the correct *feature option*
  is enabled and the *selected target/toolchain* actually requires it. Avoid unconditional/global
  flags that can break other platforms or remove the ability to disable features.
repository: Tencent/ncnn
label: Configurations
language: Txt
comments_count: 6
repository_stars: 23205
---

When changing build configuration (compiler definitions, link libraries, compile/link flags), ensure it is applied only when the correct *feature option* is enabled and the *selected target/toolchain* actually requires it. Avoid unconditional/global flags that can break other platforms or remove the ability to disable features.

Practical rules:
- Gate configuration with the project’s option (e.g., NCNN_OPENMP) and/or a precise target/toolchain condition (e.g., ANDROID_NDK vs just ANDROID).
- Prefer target-scoped, modern CMake integration (e.g., target_link_libraries with imported targets) over mutating global variables like CMAKE_CXX_FLAGS.
- Only add compile/link flags that make sense for the produced artifact type (e.g., OpenMP linking is relevant for executables/shared/module builds, not for a static library target in isolation).

Example pattern (OpenMP):
```cmake
option(NCNN_OPENMP "build with OpenMP" ON)

if(NCNN_OPENMP)
  find_package(OpenMP)
  if(OpenMP_CXX_FOUND)
    # Apply to the actual consuming target(s)
    target_link_libraries(my_executable PRIVATE OpenMP::OpenMP_CXX)
  endif()
endif()
```

Example pattern (target/toolchain gating):
```cmake
# Don’t treat any ANDROID-defined toolchain as an Android NDK build.
if(ANDROID AND ANDROID_NDK)
  # android-specific flags/libs
endif()

# Don’t force XP-only definitions for every WIN32 build.
if(WIN32 AND NCNN_TARGET_XP)
  target_compile_definitions(ncnn PUBLIC _WIN32_WINNT=0x0501 WINVER=0x0501)
endif()
```