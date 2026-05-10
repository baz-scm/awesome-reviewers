---
title: Null-safe checks
description: Make null/empty handling explicit and safe—so empty values don’t break
  logic or even generate invalid syntax, and raw null-pointer checks are replaced
  with semantic, invariant-based checks.
repository: Tencent/ncnn
label: Null Handling
language: Other
comments_count: 5
repository_stars: 23205
---

Make null/empty handling explicit and safe—so empty values don’t break logic or even generate invalid syntax, and raw null-pointer checks are replaced with semantic, invariant-based checks.

Guidelines:
1) Avoid “empty variable” syntax bugs (CMake): quote variables in comparisons.
   - Bad: `elseif(${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang")` (breaks if the variable expands to empty)
   - Good: `elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")`

2) Prefer semantic checks over raw pointer null checks (C++ containers/tensors):
   - Replace `if (ptr != NULL)` with `if (!obj.empty())` or equivalent invariants when available.
   - Example pattern: `if (!_bias.empty()) { /* use bias */ } else { /* no bias */ }`

3) Don’t over-defend against null in operations that are already null-safe:
   - `delete NULL;` is safe—unnecessary `if (ptr) delete ptr;` can be removed for clarity.

4) For null-terminated byte strings, ensure the correct terminator behavior:
   - When constructing/copying C-strings into custom buffers, allocate/copy consistently so the destination is properly null-terminated (e.g., consider whether you need `len + 1` and whether you copy `len+1`).

Applying these rules reduces crashes, undefined behavior, and correctness issues caused by missing/empty/null values.