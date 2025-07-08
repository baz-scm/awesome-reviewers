---
title: Actionable error messages
description: When writing error messages in PyTorch code, include not only what went
  wrong but also clear guidance on how to fix the issue. This helps users quickly
  understand and resolve problems without digging through documentation.
repository: pytorch/pytorch
label: Pytorch
language: C++
comments_count: 2
repository_stars: 91345
---

When writing error messages in PyTorch code, include not only what went wrong but also clear guidance on how to fix the issue. This helps users quickly understand and resolve problems without digging through documentation.

Example from tensor device operations:
```cpp
// Poor error message:
TORCH_CHECK(false, "Cannot move tensor between devices");

// Better error message with remediation:
TORCH_CHECK(
  !force_move,
  "cannot move tensor from ", 
  data.device(),
  " to ", 
  device,
  " without copying. Set copy=True is needed.");
```

This practice is especially important for operations that have non-obvious requirements or constraints, such as tensor movement between devices, shape transformations, or operations with specific dtype requirements. By providing actionable guidance directly in error messages, you improve the developer experience and reduce support burden.