---
title: Consistent Semantic Identifiers
description: When adding/changing code, use names that (1) match existing project
  conventions, (2) clearly express intent, and (3) avoid reserved/problematic identifier
  patterns.
repository: Tencent/ncnn
label: Naming Conventions
language: C++
comments_count: 8
repository_stars: 23205
---

When adding/changing code, use names that (1) match existing project conventions, (2) clearly express intent, and (3) avoid reserved/problematic identifier patterns.

Rules:
- Avoid reserved naming: do not use local variable names starting with `_` (e.g., prefer `top`, `front`, `behind` over `_top`, `_front`).
- Use semantic, intent-revealing names: avoid vague placeholders like `size_threshold`; prefer names that encode behavior/meaning (e.g., `budget_count_threshold` / `budget_drop_threshold`).
- Follow established naming patterns: use the project’s width/height/etc. suffix conventions consistently (e.g., `kernel_w`, `stride_w`, and similarly `out_w`, `out_h`).
- Align dimension/axis naming to ncnn semantics: use the same axis ordering and naming expected by the codebase (commonly `z y x` meaning dep/row/col), and ensure axis transforms follow ncnn conventions.
- Keep platform and parameter identifiers correct: use the correct architecture macro names and ensure variable/index names correspond to the documented parameter meaning/order.

Example (naming fixes):
```cpp
// Bad: reserved leading underscore + vague intent
int _top;
size_t size_threshold = 10;

// Good: non-reserved + semantic intent
int top;
size_t budget_drop_threshold = 10;

// Good: follow *_w / *_h conventions
int out_w = pd.get(18, out_h);
```