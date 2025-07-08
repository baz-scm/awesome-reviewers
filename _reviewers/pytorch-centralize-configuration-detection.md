---
title: Centralize configuration detection
description: Always use centralized configuration detection mechanisms (like CMake
  finder modules) instead of hardcoding paths or environment variables. This approach
  ensures compatibility across different installation methods and environments.
repository: pytorch/pytorch
label: Configurations
language: Shell
comments_count: 2
repository_stars: 91345
---

Always use centralized configuration detection mechanisms (like CMake finder modules) instead of hardcoding paths or environment variables. This approach ensures compatibility across different installation methods and environments.

When integrating with external libraries or tools:

1. Prefer creating dedicated finder modules (e.g., `findXXX.cmake`) that can detect installations in multiple locations
2. Avoid directly exporting environment variables in scripts that may not be universally applicable
3. Implement robust path resolution that works consistently across build environments
4. Validate that paths exist before using them in critical operations

For example, instead of hardcoding:
```bash
export NVSHMEM_HOME=/usr/local
```

Create a CMake finder module that can handle multiple installation scenarios:
```cmake
# findNVSHMEM.cmake example
find_path(NVSHMEM_INCLUDE_DIR nvshmem.h
  PATHS
    ${NVSHMEM_HOME}/include
    /usr/local/include
    $ENV{CONDA_PREFIX}/include
)

if(NVSHMEM_INCLUDE_DIR)
  get_filename_component(NVSHMEM_HOME ${NVSHMEM_INCLUDE_DIR} DIRECTORY)
endif()
```

This approach ensures your build system can adapt to different installation methods (pip, system packages, custom paths) without requiring manual configuration changes.