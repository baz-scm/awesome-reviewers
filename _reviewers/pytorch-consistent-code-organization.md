---
title: Consistent code organization
description: 'Follow consistent code organization patterns:


  1. Place static definitions in .cpp files rather than headers to prevent duplicate
  definitions when included in multiple compilation units:'
repository: pytorch/pytorch
label: Code Style
language: Other
comments_count: 3
repository_stars: 91345
---

Follow consistent code organization patterns:

1. Place static definitions in .cpp files rather than headers to prevent duplicate definitions when included in multiple compilation units:
```cpp
// Avoid in header (.hpp):
static HeartbeatMonitor* get() {
  static HeartbeatMonitor instance;
  return &instance;
}

// Prefer in implementation (.cpp):
HeartbeatMonitor* HeartbeatMonitor::get() {
  static HeartbeatMonitor instance;
  return &instance;
}
```

2. Explicitly define class semantics using appropriate macros and default specifications:
```cpp
class BiasHandler {
  C10_DISABLE_COPY_AND_ASSIGN(BiasHandler);
  
  BiasHandler(BiasHandler&&) = default;
  BiasHandler& operator=(BiasHandler&&) = default;
  
  // Class implementation...
};
```

3. Maintain consistent implementation patterns across related components (e.g., use class-based or function-based implementations consistently for similar functionality). When extending existing code, follow the established patterns from the CPU implementation or related components.