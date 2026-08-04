---
title: Consistent Identifier Naming
description: 'Use naming rules that keep identifiers consistent, unambiguous, and
  resilient to change:


  - Centralize repeated string keys/labels used as identifiers (e.g., dictionary/property-bag
  keys) into named constants so the same literal can’t drift across methods.'
repository: Azure/azure-powershell
label: Naming Conventions
language: C#
comments_count: 2
repository_stars: 4762
---

Use naming rules that keep identifiers consistent, unambiguous, and resilient to change:

- Centralize repeated string keys/labels used as identifiers (e.g., dictionary/property-bag keys) into named constants so the same literal can’t drift across methods.
  - Prefer: `private const string VmSubscriptionIdKey = "VM Subscription ID";`
  - Then use `PropertyBag.ContainsKey(VmSubscriptionIdKey)` and `PropertyBag[VmSubscriptionIdKey]`.

- Follow established naming conventions for public API surfaces (cmdlet parameters, properties), including singularity guidance.
  - If a parameter represents a single logical item, name it in singular form (e.g., `Tag`), even if the underlying type is a map/hashtable.

Example (combining both practices):
```csharp
private const string VmSubscriptionIdKey = "VM Subscription ID";

// ...
if (vmJob.ExtendedInfo.PropertyBag.ContainsKey(VmSubscriptionIdKey))
{
    detailedResponse.Properties.Add(
        VmSubscriptionIdKey,
        vmJob.ExtendedInfo.PropertyBag[VmSubscriptionIdKey]);
}

[Parameter(Mandatory = false, ValueFromPipelineByPropertyName = true)]
[Alias("Tag")]
public Hashtable Tag { get; set; }
```