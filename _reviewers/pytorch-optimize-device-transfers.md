---
title: Optimize device transfers
description: When implementing operations that transfer data between devices (particularly
  CPU to GPU), use device guards and pinned memory to optimize performance. Device
  guards ensure the correct device context, while pinned memory enables asynchronous
  data transfers.
repository: pytorch/pytorch
label: Pytorch
language: Other
comments_count: 5
repository_stars: 91169
---

When implementing operations that transfer data between devices (particularly CPU to GPU), use device guards and pinned memory to optimize performance. Device guards ensure the correct device context, while pinned memory enables asynchronous data transfers.

For device guards, always add them at the beginning of functions that operate on tensors from potentially different devices:
```cpp
// Add device guard based on input tensors
c10::DeviceGuard device_guard(input_t.device());
```

For CPU-to-GPU transfers, use pinned memory to enable non-blocking copies:
```cpp
// When transferring data from CPU to GPU
if (tensor.is_cpu() && destination.device().is_cuda()) {
  // Allocate output in pinned memory for non-blocking transfer
  auto options = tensor.options().pinned_memory(true);
  auto pinned_tensor = at::empty(tensor.sizes(), options);
  // Use pinned tensor as the output or for intermediate operations
  // ...
}
```

Provide clear error messages when operations cannot be performed without copying between devices:
```cpp
TORCH_CHECK(
  !force_move, 
  "cannot move tensor from ", source_device,
  " to ", target_device,
  " without copying. Set copy=True if needed.");
```

These optimizations significantly improve performance by reducing synchronization overhead between CPU and GPU operations.
