---
title: Document configuration logic
description: Always add clear, explanatory comments for conditional configuration
  logic, architectural decisions, and platform-specific handling. Configuration code
  often involves complex decision trees, temporary solutions during transitions, and
  platform-specific workarounds that may not be immediately obvious to other developers.
repository: facebook/react-native
label: Configurations
language: Other
comments_count: 5
repository_stars: 123178
---

Always add clear, explanatory comments for conditional configuration logic, architectural decisions, and platform-specific handling. Configuration code often involves complex decision trees, temporary solutions during transitions, and platform-specific workarounds that may not be immediately obvious to other developers.

When implementing conditional configuration logic, explain the reasoning behind the conditions and what each branch accomplishes. For architectural transitions, document the temporary nature of solutions and migration plans. For platform-specific code, explain why the special handling is necessary.

Example from CMake configuration:
```cmake
# We check if the user is providing a custom OnLoad.cpp file. If so, we pick that
# for compilation. Otherwise we fallback to using the `default-app-setup/OnLoad.cpp` 
# file instead.
if(override_cpp_SRC)
    # Use custom implementation
else()
    # Use default setup
endif()

# On Windows, backslashes in file paths are interpreted as escape characters
# Convert to forward slashes for consistent path handling across platforms
if(CMAKE_HOST_WIN32)
    string(REPLACE "\\" "/" BUILD_DIR ${BUILD_DIR})
    string(REPLACE "\\" "/" REACT_ANDROID_DIR ${REACT_ANDROID_DIR})
endif()
```

This practice prevents confusion during code reviews, helps with maintenance during architectural transitions, and makes platform-specific workarounds understandable to developers working on different operating systems.