---
title: Document code reasoning
description: 'Add clear, concise comments that explain the "why" behind complex logic,
  non-obvious decisions, and implicit behaviors. Focus on documenting:


  1. **Algorithmic choices and control flow** - Explain why loops are broken, conditions
  are checked, or specific approaches are used.'
repository: Azure/azure-sdk-for-net
label: Documentation
language: C#
comments_count: 6
repository_stars: 5809
---

Add clear, concise comments that explain the "why" behind complex logic, non-obvious decisions, and implicit behaviors. Focus on documenting:

1. **Algorithmic choices and control flow** - Explain why loops are broken, conditions are checked, or specific approaches are used.

```csharp
// Break if the next page is null
// Break the loop if the next page variable is null, indicating no more pages to process.
```

2. **Parameter handling details** - Document implicit conversions, default values, and edge cases.

```csharp
// The premiumPageBlobAccessTier parameter specifies the access tier for the page blob.
// If null, the REST API will apply the default tier or handle it gracefully.
```

3. **Version-specific logic or format handling** - Explain format parsing, version checks, or compatibility code.

```csharp
// This method checks if the format string in options.Format ends with the "|v3" suffix.
// The "|v3" suffix indicates that the ManagedServiceIdentity format is version 3.
// If the suffix is present, it is removed, and the base format is returned.
```

4. **Complex operations or type conversions** - Make non-obvious operations clear to future maintainers.

```csharp
// Convert ShareProtocols (multi-valued) to ShareProtocol (single-valued).
// If effectiveProtocol is ShareProtocols.Smb, map to ShareProtocol.Smb.
// Otherwise, default to ShareProtocol.Nfs.
```

Comments should benefit future maintainers by providing context that isn't immediately obvious from the code itself. When complex code can't be simplified, comprehensive documentation becomes essential for long-term maintainability.
