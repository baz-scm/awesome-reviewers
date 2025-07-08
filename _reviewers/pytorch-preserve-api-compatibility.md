---
title: Preserve API compatibility
description: When modifying existing APIs, always prioritize backward compatibility
  to avoid breaking client code. Before changing API signatures, function names, or
  return types, first consider the impact on existing consumers.
repository: pytorch/pytorch
label: API
language: Other
comments_count: 2
repository_stars: 91345
---

When modifying existing APIs, always prioritize backward compatibility to avoid breaking client code. Before changing API signatures, function names, or return types, first consider the impact on existing consumers.

If an API needs new functionality:
1. Add new functions rather than modifying existing ones
2. Mark old functions as deprecated before eventual removal
3. Document migration paths clearly

For new APIs, consider future compatibility:
- Avoid prematurely exposing implementation details with public visibility markers (like `C10_API`)
- Only expose interfaces as public when there's clear evidence they need external access

Example from the discussions:
```cpp
// Instead of changing an existing function signature:
// TORCH_API DLManagedTensor* toDLPack(const Tensor& src);
// -> TORCH_API DLManagedTensorVersioned* toDLPack(const Tensor& src);

// Prefer adding a new function while preserving the original:
TORCH_API DLManagedTensor* toDLPack(const Tensor& src);  // Maintain original
TORCH_API DLManagedTensorVersioned* toDLPackV2(const Tensor& src);  // Add new version
```

This approach ensures libraries using your API can upgrade on their own timeline and prevents unexpected runtime failures.