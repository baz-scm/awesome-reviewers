---
title: Canonical Naming and Typos
description: Use canonical, consistently formatted identifiers across code and build
  files, and verify every variable/option name is spelled exactly as the build system
  expects.
repository: Tencent/ncnn
label: Naming Conventions
language: Txt
comments_count: 3
repository_stars: 23205
---

Use canonical, consistently formatted identifiers across code and build files, and verify every variable/option name is spelled exactly as the build system expects.

Apply this checklist:
1) Canonical token per platform/arch: follow the established external style the project aligns with (e.g., for Loongarch, prefer `loongarch` consistently rather than `loongarch64` for directory/file/class naming).
2) Consistent formatting for feature/option names: follow existing project patterns for suffixes (e.g., prefer `NCNN_SSE41` over `NCNN_SSE4_1` to match conventions like `NCNN_ARM82`, `NCNN_ARM86XXX`).
3) Typo-proof build identifiers: for CMake, use the exact variable names (typos silently break behavior). 

Example (CMake):
```cmake
# Bad (typo)
set(CMAKE_EXECUTBLE_LINKER_FLAGS "${CMAKE_EXECUTBLE_LINKER_FLAGS} ...")

# Good
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -s FORCE_FILESYSTEM=1")

# Good option naming
option(NCNN_SSE41 "optimize ... with sse4.1 extension" ON)
```