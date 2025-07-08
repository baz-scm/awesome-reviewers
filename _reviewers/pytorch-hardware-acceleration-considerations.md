---
title: Hardware acceleration considerations
description: When implementing hardware-accelerated operations for AI models, ensure
  support for the latest architectures while considering determinism requirements.
repository: pytorch/pytorch
label: AI
language: Other
comments_count: 2
repository_stars: 91345
---

When implementing hardware-accelerated operations for AI models, ensure support for the latest architectures while considering determinism requirements.

1. Keep architecture support up-to-date: Regularly update code to support new hardware architectures (like the latest CUDA architectures for NVIDIA GPUs or optimized paths for specialized hardware).

```cpp
// Example: Ensure architecture lists include the latest generations
// Don't forget to add new architectures like Blackwell
elseif(${arch_name} STREQUAL "Ampere")
  set(arch_bin 8.0)
  set(arch_ptx 8.0)
elseif(${arch_name} STREQUAL "Hopper")
  set(arch_bin 9.0)
  set(arch_ptx 9.0)
elseif(${arch_name} STREQUAL "Blackwell")
  set(arch_bin 10.0)
  set(arch_ptx 10.0)
```

2. Consider determinism: When implementing operations with atomic updates (like pooling operations), evaluate if they're deterministic. If not, provide alternatives or mark them appropriately for users requiring deterministic algorithms.

```cpp
// When implementing operations with potential non-determinism:
// 1. Document the non-deterministic behavior
// 2. Consider providing a deterministic alternative implementation
// 3. Add appropriate flags for torch.use_deterministic_algorithms()

// Example for pooling operations:
if (at::globalContext().deterministicAlgorithms() && 
    requires_deterministic_implementation) {
  // Use deterministic implementation (might be slower)
} else {
  // Use potentially faster non-deterministic implementation with atomics
  AtomicType<T>::atomic_add(...);
}
```

Hardware-optimized implementations significantly impact AI model performance, but must be balanced with requirements for reproducibility in research and production deployments.