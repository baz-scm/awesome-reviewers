---
title: consolidate duplicated logic
description: When you identify duplicated code patterns across different branches
  or functions, consolidate the shared logic into a unified implementation to improve
  maintainability and reduce code bloat. This applies whether the duplication occurs
  within conditional branches, across similar functions, or in separate files.
repository: sgl-project/sglang
label: Code Style
language: CUDA
comments_count: 2
repository_stars: 17245
---

When you identify duplicated code patterns across different branches or functions, consolidate the shared logic into a unified implementation to improve maintainability and reduce code bloat. This applies whether the duplication occurs within conditional branches, across similar functions, or in separate files.

For substantial duplication, extract the common logic into a shared function or kernel. For minimal implementations (a dozen lines or less), consider inlining the logic using C++ templates and constexpr to avoid overhead while maintaining clarity.

Example of consolidation:
```cpp
// Before: Duplicated logic in branches
if (params.VPT <= 32) {
    // Complex processing logic A
    // ... 50 lines of similar code
} else {
    // Complex processing logic B  
    // ... 50 lines of nearly identical code
}

// After: Consolidated into unified kernel
template<bool small_vpt>
void unified_processing_kernel(...) {
    // Shared logic with template specialization
    if constexpr (small_vpt) {
        // Small VPT specific optimizations
    } else {
        // Large VPT specific optimizations  
    }
}
```

This approach reduces maintenance burden, minimizes the risk of inconsistent updates, and keeps the codebase clean and organized.