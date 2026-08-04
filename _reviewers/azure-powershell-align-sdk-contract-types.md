---
title: Align SDK contract types
description: 'When updating generated PowerShell/SDK clients (e.g., AutoRest v3 →
  v4), treat the generated model contract as authoritative: match namespaces/types
  and ensure request serialization shape matches what the REST service expects.'
repository: Azure/azure-powershell
label: API
language: Other
comments_count: 5
repository_stars: 4762
---

When updating generated PowerShell/SDK clients (e.g., AutoRest v3 → v4), treat the generated model contract as authoritative: match namespaces/types and ensure request serialization shape matches what the REST service expects.

**Do**
- Update type references to the v4 flattened namespaces (don’t keep v3 versioned model types).
- Apply enum→string and other contract-shaped changes in parameters as-is.
- For parameters involving collections/identity dictionaries, preserve the generated model shape. If the SDK now defines `String[]`, it will serialize as an array—AutoRest will not convert that into a hashtable/dictionary.
- Update tests to assert fields based on the API version actually used (and use instance view expansions when required). Prefer SDK cmdlets for assertions when they expose the property; otherwise assert via REST for the missing fields.

**Don’t**
- Assume backwards-compatible behavior (e.g., that a hashtable input will still be produced, or that enum-typed parameters can remain unchanged).

**Example (identity shape change)**
```powershell
# AutoRest v4 style: array of ARM resource IDs
[Parameter(Mandatory=$false)]
[System.String[]] $UserAssignedIdentity

# SDK will serialize $UserAssignedIdentity as a JSON array.
# If the service still expects a dictionary/hashtable payload,
# update the service contract instead of trying to “fix” it in the cmdlet.
```

Use this checklist during migrations and related API interface work to avoid subtle request/response contract breaks and mismatched serialization payloads.