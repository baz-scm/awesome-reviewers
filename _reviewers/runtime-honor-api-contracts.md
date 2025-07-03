---
title: Honor API contracts
description: When implementing or modifying APIs, carefully preserve the historical
  behavior and semantic contracts of existing interfaces, even when those behaviors
  seem counterintuitive. This includes maintaining consistent exception throwing patterns
  and honoring the distinct purposes of method overloads.
repository: dotnet/runtime
label: API
language: C#
comments_count: 2
repository_stars: 16578
---

When implementing or modifying APIs, carefully preserve the historical behavior and semantic contracts of existing interfaces, even when those behaviors seem counterintuitive. This includes maintaining consistent exception throwing patterns and honoring the distinct purposes of method overloads.

For example, when implementing overloaded methods:
```csharp
// Different overloads may have subtly different semantics by design
// This overload conditionally includes entries based on trimTarget being marked
public void AddExternalTypeMapEntry(string name, Type target, Type trimTarget) {
    // Only include if trimTarget is marked
    if (IsTrimTargetMarked(trimTarget)) {
        RecordTypeMapEntry(name, target);
    }
}

// While this overload is meant as an "escape hatch" with unconditional behavior
public void AddExternalTypeMapEntry(string name, Type target) {
    // Always include this entry regardless of other conditions
    RecordTypeMapEntry(name, target);
}
```

Similarly, maintain expected exception behaviors. If an API historically throws for certain inputs (like Sign throwing for NaN values), preserve this pattern even if it seems inconsistent with similar methods. These behaviors form part of the API's contract that users may depend on.
