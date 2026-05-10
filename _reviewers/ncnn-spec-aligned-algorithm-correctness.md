---
title: Spec-aligned Algorithm Correctness
description: All algorithm implementations must be spec-aligned for the exact operator
  variant, tensor shapes/axes, and boundary conditions. Before merging, developers
  should explicitly verify that special cases and out-of-bound behavior follow the
  framework/ONNX semantics; avoid “one-size-fits-all” code paths that silently produce
  wrong results.
repository: Tencent/ncnn
label: Algorithms
language: C++
comments_count: 8
repository_stars: 23205
---

All algorithm implementations must be spec-aligned for the exact operator variant, tensor shapes/axes, and boundary conditions. Before merging, developers should explicitly verify that special cases and out-of-bound behavior follow the framework/ONNX semantics; avoid “one-size-fits-all” code paths that silently produce wrong results.

Apply these checks:
1) Operator variant semantics must match the spec
- If an operator has multiple semantics (e.g., hard vs soft shrink), implement them separately or with a correctness-preserving conditional.

2) Boundary/padding modes must apply to every sampled neighbor
- For sampling/interpolation/grid ops, out-of-bound neighbor handling must respect padding_mode/align_corner. It’s not enough to “fix the coordinate”; the neighbor value lookup must also follow the same padding behavior.

3) Use integer-safe floor/ceil for index mapping
- When converting continuous output coordinates to input indices, prefer integer arithmetic that matches floor/ceil definitions to avoid float rounding issues.
  Example pattern (floor/ceil div):
  ```cpp
  // floor div: ih0 = floor(h*i/out_h)
  int ih0 = (h * i) / out_h;
  // ceil div: ih1 = ceil(h*(i+1)/out_h)
  int ih1 = (h * (i + 1) + out_h - 1) / out_h;
  ```

4) Shape/axis/loop structure must match the actual Mat layout
- When axis-specific behavior exists (e.g., InnerProduct), ensure loops cover all required dimensions and writes target the correct logical indices (don’t assume a 2D layout when the tensor is 3D+).

5) Special cases must not be routed through general logic
- If an input is a vector/1D tensor (or any other structural special case), ignore unrelated parameters (e.g., resize_type) and keep that logic in a dedicated branch.

6) Output type must match the source spec
- If the spec defines an integer tensor output, don’t return float to “approximate”; confirm downstream layers won’t break on precision or type assumptions.

7) Add minimal correctness tests
- For each algorithmic change, include at least one test case per (a) variant (hard/soft, avg/max), (b) padding_mode/boundary scenario, and (c) axis/shape configuration, plus a “large value” case for integer-typed specs.