---
title: Feature flag convention
description: 'Establish a consistent pattern for feature flags and dependency management
  in configuration files:


  1. Use `WITH_*` or `OPENCV_ENABLE_*` variables to represent user intentions (features
  to enable if available)'
repository: opencv/opencv
label: Configurations
language: Txt
comments_count: 3
repository_stars: 82865
---

Establish a consistent pattern for feature flags and dependency management in configuration files:

1. Use `WITH_*` or `OPENCV_ENABLE_*` variables to represent user intentions (features to enable if available)
2. Perform proper detection with `find_package()` and preferably `try_compile()` to validate dependencies
3. Set `HAVE_*` variables based on actual availability check results
4. Always guard feature usage in code with `HAVE_*` checks
5. Prefer target-based dependencies over simple flag checks
6. Make compile definitions PUBLIC when they affect interface headers

Example:
```cmake
# User intention
ocv_option(OPENCV_ENABLE_EGL_INTEROP "Build with EGL interoperability support" ON)

# Actual detection (in main CMakeLists.txt)
if(OPENCV_ENABLE_EGL_INTEROP)
  find_package(EGL)
  if(EGL_FOUND)
    set(HAVE_EGL_INTEROP ON)
  endif()
endif()

# Usage in module CMakeLists.txt
if(HAVE_EGL_INTEROP)
  # Prefer target-based dependencies
  target_link_libraries(${the_module} PUBLIC ocv.3rdparty.egl)
  # Make definitions PUBLIC if used in headers
  target_compile_definitions(${the_module} PUBLIC HAVE_EGL_INTEROP)
endif()
```

This convention ensures all dependencies are properly detected during configuration stage, not build stage, preventing build failures due to missing dependencies. It clearly separates user intent from actual availability and promotes modern CMake practices.
