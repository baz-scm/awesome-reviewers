---
title: match API complexity appropriately
description: Design APIs with complexity that matches their actual use cases and adopt
  established patterns that improve clarity. Avoid over-engineering interfaces when
  simpler alternatives suffice, and prefer modern, well-established patterns over
  legacy approaches.
repository: llvm/llvm-project
label: API
language: Other
comments_count: 2
repository_stars: 33702
---

Design APIs with complexity that matches their actual use cases and adopt established patterns that improve clarity. Avoid over-engineering interfaces when simpler alternatives suffice, and prefer modern, well-established patterns over legacy approaches.

When designing function parameters, choose the simplest form that meets current requirements rather than anticipating future complexity that may never materialize. For example, use boolean flags instead of function callbacks when the callback would only return true/false.

For error handling, prefer modern patterns like Expected<T> over output parameters combined with status codes, as they provide clearer semantics and better composability.

Example of simplification:
```cpp
// Instead of complex callback for simple cases:
bool LoopRotation(Loop *L, ..., 
    function_ref<bool(Loop *, ScalarEvolution *)> ProfitabilityCheck);

// Use simple boolean when that's all that's needed:
bool LoopRotation(Loop *L, ..., bool IgnoreProfitability);
```

Example of modern error handling:
```cpp
// Instead of output parameter + status:
static Status ResolveDeviceID(const std::string &device_id, 
                             std::string &resolved_device_id);

// Use Expected<T> pattern:
static llvm::Expected<std::string> ResolveDeviceID(llvm::StringRef device_id);
```