---
title: optimize computational efficiency
description: Prioritize algorithmic efficiency and avoid unnecessary computational
  overhead in performance-critical code paths. Look for opportunities to reduce time
  complexity and eliminate redundant calculations.
repository: hyprwm/Hyprland
label: Algorithms
language: C++
comments_count: 5
repository_stars: 28863
---

Prioritize algorithmic efficiency and avoid unnecessary computational overhead in performance-critical code paths. Look for opportunities to reduce time complexity and eliminate redundant calculations.

Key optimization strategies:
- Use squared distance instead of actual distance when only comparison is needed: `prefer distanceSq` over `distance()` for performance-critical geometric calculations
- Avoid nested loops when a single pass is sufficient: instead of O(rules × workspaces) complexity, optimize to O(rules) by tracking only changed elements
- Eliminate redundant calculations by caching or restructuring computation order
- Choose appropriate STL algorithms: use `std::erase_if` directly instead of the `std::ranges::remove_if` + `erase` pattern when possible

Example from distance calculations:
```cpp
// Instead of:
if (m_vBeginDragXY.distance(mousePos) <= *PDRAGTHRESHOLD)

// Use:
if (m_vBeginDragXY.distanceSq(mousePos) <= (*PDRAGTHRESHOLD * *PDRAGTHRESHOLD))
```

Example from workspace checking:
```cpp
// Instead of checking all workspaces against all rules O(n*m):
for (auto& workspace : workspaces) {
    for (auto& rule : rules) { /* check */ }
}

// Optimize to O(n) by checking only the changed workspace:
recheckPersistent(); // Only checks current workspace against rules
```

This approach reduces CPU cycles in frequently called functions and improves overall application responsiveness.