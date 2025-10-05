---
title: Cache expensive operations
description: Identify operations that are expensive and called frequently, then optimize
  them by caching results, moving to appropriate lifecycle events, or replacing with
  faster alternatives. Expensive operations like parameter reads, system calls, or
  complex computations should not be repeated unnecessarily in hot code paths.
repository: commaai/openpilot
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 58214
---

Identify operations that are expensive and called frequently, then optimize them by caching results, moving to appropriate lifecycle events, or replacing with faster alternatives. Expensive operations like parameter reads, system calls, or complex computations should not be repeated unnecessarily in hot code paths.

For example, instead of calling expensive parameter reads on every update:
```cpp
// Avoid: Called on every update (expensive)
bool AnnotatedCameraWidget::isDMAlwaysOn() const {
  Params params;
  return params.getBool("AlwaysOnDM");  // params.get() is expensive
}
```

Move the expensive operation to initialization or appropriate lifecycle events:
```cpp
// Better: Update once when widget becomes visible
void AnnotatedCameraWidget::showEvent(QShowEvent *event) {
  Params params;
  dm_always_on = params.getBool("AlwaysOnDM");  // Cache the result
}
```

Similarly, replace slow system operations with faster alternatives when available. A 16ms operation replaced with a 0.5ms equivalent can significantly improve responsiveness in frequently called code paths.