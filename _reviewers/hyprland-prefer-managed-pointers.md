---
title: prefer managed pointers
description: Raw pointers are banned in new code unless absolutely necessary. Instead,
  use managed pointer types to prevent null pointer dereferences, dangling pointers,
  and memory safety issues.
repository: hyprwm/Hyprland
label: Null Handling
language: Other
comments_count: 4
repository_stars: 28863
---

Raw pointers are banned in new code unless absolutely necessary. Instead, use managed pointer types to prevent null pointer dereferences, dangling pointers, and memory safety issues.

Use the appropriate managed pointer type based on ownership semantics:
- `SP<T>` (shared pointer) for shared ownership
- `UP<T>` (unique pointer) for exclusive ownership  
- `WP<T>` (weak pointer) for non-owning references

Example from the codebase:
```cpp
// Bad - raw pointer prone to null dereferences
CExtWorkspaceHandleV1* workspace;
SSessionLockSurface* touchFocusLockSurface;
CXxColorManagementSurfaceV4* m_pCMSurface = nullptr;

// Good - managed pointers prevent null issues
SP<CExtWorkspaceHandleV1> workspace;
WP<SSessionLockSurface> touchFocusLockSurface;  
WP<CXxColorManagementSurfaceV4> m_pCMSurface;
```

For protocol implementations, prefer `UP<>` for resource ownership while allowing `WP<>` references to it. This pattern ensures proper lifetime management and prevents accessing freed memory.