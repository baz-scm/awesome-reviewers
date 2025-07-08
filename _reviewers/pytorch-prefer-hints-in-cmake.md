---
title: Prefer HINTS in CMake
description: When configuring library searches in CMake, use `HINTS` instead of `PATHS`
  when you want to prioritize specific locations before falling back to system defaults.
  `HINTS` are searched before default paths, while `PATHS` are searched after default
  paths. This ensures that user-specified or environment-provided paths are checked
  first, making dependency...
repository: pytorch/pytorch
label: Configurations
language: Txt
comments_count: 3
repository_stars: 91345
---

When configuring library searches in CMake, use `HINTS` instead of `PATHS` when you want to prioritize specific locations before falling back to system defaults. `HINTS` are searched before default paths, while `PATHS` are searched after default paths. This ensures that user-specified or environment-provided paths are checked first, making dependency resolution more predictable.

Include common path suffixes to improve the robustness of library discovery:

```cmake
find_library(NVSHMEM_HOST_LIB
  # In pip install case, the lib suffix is `.so.3` instead of `.so`
  NAMES nvshmem_host nvshmem_host.so.3
  HINTS $ENV{NVSHMEM_HOME} ${NVSHMEM_PY_DIR}
  PATH_SUFFIXES lib lib64 cuda/lib cuda/lib64 lib/x64
  DOC "The location of NVSHMEM host library.")
```

This approach creates a more reliable search order:
1. First check HINTS locations with their suffixes
2. Then check standard system locations
3. Finally check PATHS locations if specified

Using this pattern helps avoid unexpected library resolution and ensures dependencies are found in the correct locations, especially in complex build environments with multiple library versions.