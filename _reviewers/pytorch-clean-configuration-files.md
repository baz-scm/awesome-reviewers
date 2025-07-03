---
title: Clean configuration files
description: "Maintain clean and readable configuration files by removing obsolete\
  \ settings and using clear, maintainable paths. \n\nKey practices:\n1. Regularly\
  \ review and remove configuration options for unsupported platforms or deprecated\
  \ features"
repository: pytorch/pytorch
label: Configurations
language: Txt
comments_count: 3
repository_stars: 91169
---

Maintain clean and readable configuration files by removing obsolete settings and using clear, maintainable paths. 

Key practices:
1. Regularly review and remove configuration options for unsupported platforms or deprecated features
2. Use absolute paths from the project root rather than deep, complex relative paths
3. Provide specific, descriptive labels for build options and configuration flags

Example - Instead of:
```cmake
# Overly complex relative path
execute_process(
  COMMAND python3 ${CMAKE_CURRENT_LIST_DIR}/../../../../../../../../third_party/composable_kernel/example/ck_tile/01_fmha/generate.py
)

# Vague option description
cmake_dependent_option(USE_ROCM_CK_GEMM "Use ROCm Composable Kernel" ON "USE_ROCM" OFF)
```

Prefer:
```cmake
# Clear path from project root
execute_process(
  COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/third_party/composable_kernel/example/ck_tile/01_fmha/generate.py
)

# Specific option description
cmake_dependent_option(USE_ROCM_CK_GEMM "Use ROCm Composable Kernel for GEMMs" ON "USE_ROCM" OFF)
```
