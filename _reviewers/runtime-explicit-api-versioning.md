---
title: Explicit API versioning
description: When extending interfaces with new methods or functionality, always implement
  proper versioning to ensure compatibility across different clients. Breaking changes
  should increment major versions, while additive changes should increment minor versions.
  More importantly, implement version checks in your code to gracefully handle compatibility.
repository: dotnet/runtime
label: API
language: Other
comments_count: 2
repository_stars: 16578
---

When extending interfaces with new methods or functionality, always implement proper versioning to ensure compatibility across different clients. Breaking changes should increment major versions, while additive changes should increment minor versions. More importantly, implement version checks in your code to gracefully handle compatibility.

For example, when adding a new method to an interface:

```csharp
// 1. Update the version constant when adding functionality
#define API_INTERFACE_MAJOR_VERSION 2  // Increment for breaking changes
#define API_INTERFACE_MINOR_VERSION 5  // Increment for non-breaking additions

// 2. Implement version checks in code that calls the new functionality
if (runtimeVersion >= API_INTERFACE_MAJOR_VERSION) {
    // Call new method safely knowing it exists
    interface.NewMethod();
} else {
    // Provide alternative implementation or graceful degradation
    FallbackImplementation();
}
```

This approach allows clients on older versions to continue functioning when interacting with newer APIs and vice versa. Remember that versioning is only useful if actively checked during runtime - simply incrementing version numbers without implementing corresponding checks provides no actual compatibility benefits.
