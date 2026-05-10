---
title: Intentional Test Coverage
description: 'All unit tests should be (1) intentionally designed for coverage, (2)
  non-redundant, and (3) maintainable.


  Apply these rules:


  1) Enforce correctness with invariants'
repository: Tencent/ncnn
label: Testing
language: C++
comments_count: 4
repository_stars: 23205
---

All unit tests should be (1) intentionally designed for coverage, (2) non-redundant, and (3) maintainable.

Apply these rules:

1) Enforce correctness with invariants
- When the system under test has known relationships, assert them directly and return a clear error code on violation.
- Example (CPU topology):
  ```cpp
  int cpucount = ncnn::get_cpu_count();
  int bigcpucount = ncnn::get_big_cpu_count();
  int littlecpucount = ncnn::get_little_cpu_count();

  if (bigcpucount + littlecpucount != cpucount || bigcpucount > cpucount || !(littlecpucount < cpucount))
      return -1;
  ```

2) Cover critical tensor ranks/shapes, not just “typical” ones
- If a layer/operator supports multiple ranks or expects specific dimensionalities, add targeted tests for the missing ranks (e.g., 1D and 4D when relevant).
- Make rank coverage a checklist item when adding/adjusting operator tests.

3) Reuse shared test helpers for layer/model execution
- Prefer existing generic helpers (e.g., a `test_layer<>`-style utility) instead of duplicating manual layer creation, parameter loading, pipeline creation, and forward logic.
- Only write bespoke setup when the helper cannot express the needed test scenario.

4) Remove duplicated or near-identical test cases
- Deduplicate test vectors/case lists. If new cases are added, ensure they add distinct coverage (different shapes/parameters/edge conditions), rather than repeating the same configuration.
- If duplication is discovered, consolidate into a parameterized list or a shared test case generator.

Result: tests become smaller, faster to review, easier to maintain, and less likely to miss regressions due to missing shape variants or redundant cases.