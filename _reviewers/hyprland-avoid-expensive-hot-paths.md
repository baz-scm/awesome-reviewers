---
title: avoid expensive hot paths
description: Identify and optimize expensive operations in frequently executed code
  paths to prevent performance bottlenecks. Hot paths include rendering loops, input
  event handlers, and frequently called utility functions.
repository: hyprwm/Hyprland
label: Performance Optimization
language: C++
comments_count: 7
repository_stars: 28863
---

Identify and optimize expensive operations in frequently executed code paths to prevent performance bottlenecks. Hot paths include rendering loops, input event handlers, and frequently called utility functions.

Key optimization strategies:
1. **Cache expensive results**: Store results of expensive operations (system calls, config lookups, X server queries) and reuse them instead of recalculating
2. **Early bailout conditions**: Add early return statements to skip unnecessary work when conditions aren't met
3. **Move expensive operations out of loops**: Relocate costly operations like config lookups to initialization or setup phases

Example of caching expensive system calls:
```cpp
static bool checkDrmSyncobjTimelineSupport(int drmFD) {
    static bool cached = false;
    static bool result = false;
    if (!cached) {
        uint64_t cap = 0;
        int ret = drmGetCap(drmFD, DRM_CAP_SYNCOBJ_TIMELINE, &cap);
        result = (ret == 0 && cap != 0);
        cached = true;
    }
    return result;
}
```

Example of early bailout optimization:
```cpp
void damageEntireParent() {
    CBox box = getParentBox();
    if (box.empty())  // Skip expensive damage calculation
        return;
    g_pHyprRenderer->damageBox(box);
}
```

Avoid config lookups in hot paths like input handlers - instead store values in object state during initialization. This prevents "extreme performance kill" scenarios where expensive operations execute on every mouse movement or render frame.