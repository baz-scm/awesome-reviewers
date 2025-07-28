---
title: Use environment variables
description: Prefer environment variables over hardcoded paths and configuration values
  in build scripts and configuration files. This approach improves portability, flexibility,
  and maintainability by allowing different environments to specify their own paths
  without modifying the codebase.
repository: ggml-org/llama.cpp
label: Configurations
language: Txt
comments_count: 2
repository_stars: 83559
---

Prefer environment variables over hardcoded paths and configuration values in build scripts and configuration files. This approach improves portability, flexibility, and maintainability by allowing different environments to specify their own paths without modifying the codebase.

Instead of hardcoding paths like:
```cmake
set(oneCCL_DIR "/opt/intel/oneapi/ccl/latest/lib/cmake/oneCCL")
set(MPI_INCLUDE_PATH "/opt/intel/oneapi/mpi/latest/include")
```

Use environment variables:
```cmake
set(oneCCL_DIR "$ENV{ONEAPI_ROOT}/ccl/latest/lib/cmake/oneCCL")
set(MPI_INCLUDE_PATH "$ENV{ONEAPI_ROOT}/mpi/latest/include")
```

For debug options and feature flags, check environment variables instead of adding compile-time options. This allows runtime configuration without rebuilding and follows established patterns like `GGML_SCHED_DEBUG`. Environment variables make configurations more flexible across different deployment environments and reduce the need for environment-specific build modifications.