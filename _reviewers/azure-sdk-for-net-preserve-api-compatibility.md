---
title: Preserve API compatibility
description: "When evolving APIs, maintain backward compatibility to prevent breaking\
  \ changes for existing consumers. \n\nKey approaches:\n\n1. **Retain removed members\
  \ with obsolete attributes**: When removing or replacing public methods, mark the\
  \ original as obsolete but maintain its functionality."
repository: Azure/azure-sdk-for-net
label: API
language: C#
comments_count: 5
repository_stars: 5809
---

When evolving APIs, maintain backward compatibility to prevent breaking changes for existing consumers. 

Key approaches:

1. **Retain removed members with obsolete attributes**: When removing or replacing public methods, mark the original as obsolete but maintain its functionality.

```csharp
// Old method
[EditorBrowsable(EditorBrowsableState.Never)]
[Obsolete("Use UpdateAsync(WaitUntil, ConnectorPatch) instead")]
public virtual Response<ConnectorResource> Update(ConnectorPatch patch, 
    CancellationToken cancellationToken = default)
{
    // Call the new implementation
    return UpdateAsync(WaitUntil.Completed, patch, cancellationToken).EnsureCompleted();
}

// New method
public virtual ArmOperation<ConnectorResource> Update(WaitUntil waitUntil, 
    ConnectorPatch patch, CancellationToken cancellationToken = default)
```

2. **Handle constructor parameter changes**: When a required parameter becomes optional, keep a constructor overload that accepts the previously required parameter:

```csharp
// Old constructor required publisherId
public MarketplaceDetails(string planId, string offerId, string publisherId) 
    : this(planId, offerId)
{
    PublisherId = publisherId;
}

// New constructor makes publisherId optional
public MarketplaceDetails(string planId, string offerId) { }
```

3. **Add code-gen attributes for serialization**: When properties are removed from models, use code generation attributes to maintain serialization compatibility:

```csharp
[CodeGenSerialization(nameof(BlockResponseCode), "blockResponseCode")]
public partial class DnsSecurityRuleAction
{
    [EditorBrowsable(EditorBrowsableState.Never)]
    public BlockResponseCode? BlockResponseCode { get; set; }
}
```

These approaches ensure that existing code continues to work while allowing APIs to evolve with improved designs.
