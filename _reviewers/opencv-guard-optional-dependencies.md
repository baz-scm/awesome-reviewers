---
title: Guard optional dependencies
description: Configuration management requires careful handling of optional dependencies
  in both build scripts and source code. Always guard code that depends on optional
  modules or libraries with appropriate feature guards, and check for component existence
  before using them.
repository: opencv/opencv
label: Configurations
language: Other
comments_count: 5
repository_stars: 82865
---

Configuration management requires careful handling of optional dependencies in both build scripts and source code. Always guard code that depends on optional modules or libraries with appropriate feature guards, and check for component existence before using them.

In build scripts:
```cmake
# Check for optional components before using them
FIND_LIBRARY(WEBP_MUX_LIBRARY NAMES webpmux)
if(WEBP_MUX_LIBRARY)
  SET(WEBP_LIBRARIES ${WEBP_LIBRARIES} ${WEBP_MUX_LIBRARY})
endif()
```

In header files:
```cpp
// Guard features that depend on optional modules
#ifdef HAVE_OPENCV_DNN
// DNN-dependent code here
#endif
```

For configuration variables, use standardized naming conventions:
- `HAVE_` prefix for feature availability (e.g., `HAVE_ZLIB` instead of `ZLIB_FOUND`)
- `OPENCV_` prefix for OpenCV-specific settings to avoid conflicts (e.g., `OPENCV_ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES`)

When detecting incompatible dependencies, provide clear messages and fallback options:
```cmake
if(HAVE_CXX17 AND OPENEXR_VERSION VERSION_LESS "2.3.0")
  message(STATUS "OpenEXR(ver ${OPENEXR_VERSION}) doesn't support C++17. Updating OpenEXR 2.3.0+ is required.")
  # Provide fallback or clear error
endif()
```
