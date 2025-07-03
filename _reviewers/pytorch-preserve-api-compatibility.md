---
title: Preserve API compatibility
description: When modifying existing APIs, ensure backward compatibility to prevent
  breaking dependent code. Changes to function signatures, return types, or visibility
  can silently break client code in ways that are difficult to detect.
repository: pytorch/pytorch
label: API
language: Other
comments_count: 4
repository_stars: 91169
---

When modifying existing APIs, ensure backward compatibility to prevent breaking dependent code. Changes to function signatures, return types, or visibility can silently break client code in ways that are difficult to detect.

To maintain compatibility:

1. **Add default parameters** when extending function signatures:
   ```cpp
   // Before:
   void emptyCache() override;
   
   // After (maintains compatibility):
   void emptyCache(c10::cuda::MempoolId_t id = {0, 0}) override;
   ```

2. **Keep original function versions** alongside new ones when changing return types:
   ```cpp
   // Original API (keep for compatibility)
   TORCH_API DLManagedTensor* toDLPack(const Tensor& src);
   
   // New versioned API (add alongside)
   TORCH_API DLManagedTensorVersioned* toDLPackVersioned(const Tensor& src);
   ```

3. **Mark shared functions with proper export attributes** (like TORCH_API) when they're called across module boundaries to ensure proper symbol visibility:
   ```cpp
   // Functions called from other modules need export markers
   TORCH_API std::unordered_set<c10::DeviceType>& GetBackendMetaAllowlist();
   ```

4. **Provide transitional paths** when implementing breaking ABI changes, allowing consumers to opt-in to new versions:
   ```cpp
   // Keep unversioned API for backward compatibility
   {"_to_dlpack", THPModule_toDLPack, METH_O, nullptr},
   // Add new versioned API that clients can use when ready
   {"_to_dlpack_unversioned", THPModule_toDLPackUnversioned, METH_O, nullptr},
   ```

When compatibility cannot be maintained, clearly document the breaking change and increment the major version number appropriately.
