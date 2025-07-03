---
title: Document function contracts
description: Always document function contracts completely, even when surrounding
  code lacks documentation. Include header comments that describe the function's purpose
  and behavior, and explicitly specify preconditions using appropriate annotations
  (like `PRECONDITION`) to clarify execution requirements.
repository: dotnet/runtime
label: Documentation
language: C++
comments_count: 2
repository_stars: 16578
---

Always document function contracts completely, even when surrounding code lacks documentation. Include header comments that describe the function's purpose and behavior, and explicitly specify preconditions using appropriate annotations (like `PRECONDITION`) to clarify execution requirements.

For example:

```cpp
// Processes cross-component references during garbage collection
// Returns true if any references were processed
void Interop::TriggerClientBridgeProcessing(
    _In_ size_t sccsLen,
    _In_ StronglyConnectedComponent* sccs,
    _In_ size_t ccrsLen,
    _In_ ComponentCrossReference* ccrs)
{
    CONTRACTL
    {
        NOTHROW;
        GC_NOTRIGGER;
        PRECONDITION(g_GCBridgeActive && "Must be called during GC suspension");
    }
    CONTRACTL_END;
    
    // Implementation...
}
```

Clear function documentation improves code readability, facilitates maintenance, and helps other developers understand code execution requirements without having to trace through all callers. Even when existing code lacks proper documentation, always document new functions completely to establish better practices over time.
