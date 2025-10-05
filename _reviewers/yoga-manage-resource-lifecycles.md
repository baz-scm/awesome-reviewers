---
title: Manage resource lifecycles
description: Ensure proper resource allocation and cleanup pairing, and maintain clear
  ownership semantics to prevent memory leaks and null reference issues. When allocating
  resources like GCHandle, always pair allocation with corresponding cleanup calls.
  Avoid overwriting allocated resources without first cleaning up the previous allocation.
repository: facebook/yoga
label: Null Handling
language: C#
comments_count: 2
repository_stars: 18255
---

Ensure proper resource allocation and cleanup pairing, and maintain clear ownership semantics to prevent memory leaks and null reference issues. When allocating resources like GCHandle, always pair allocation with corresponding cleanup calls. Avoid overwriting allocated resources without first cleaning up the previous allocation.

Additionally, use return types that clearly indicate ownership. Return IntPtr for references you don't own, and use strongly-typed handles only when your code manages the resource lifecycle.

Example of problematic code:
```csharp
public void SetMeasureFunction(MeasureFunction measureFunction) {
    var handle = GCHandle.Alloc(this); // Never freed!
    Native.YGNodeSetContext(_ygNode, GCHandle.ToIntPtr(handle));
}

public void SetBaselineFunction(BaselineFunction baselineFunction) {
    var handle = GCHandle.Alloc(this); // Overwrites previous without cleanup!
    Native.YGNodeSetContext(_ygNode, GCHandle.ToIntPtr(handle));
}
```

Better approach: Track allocated handles and free them before allocating new ones, or use return types like IntPtr when you don't own the underlying resource to avoid confusion about lifecycle responsibilities.