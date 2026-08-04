---
title: Use Standard Entity Identifiers
description: When creating `entityMappings`, use semantically strong, standard identifier
  fields as the mapped `columnName`. Avoid “legacy/weak” intermediary names like `AccountCustomEntity`
  (and avoid unnecessary wrapper columns like `IPCustomEntity`) when a direct standard
  field already exists.
repository: Azure/Azure-Sentinel
label: Naming Conventions
language: Yaml
comments_count: 6
repository_stars: 6042
---

When creating `entityMappings`, use semantically strong, standard identifier fields as the mapped `columnName`. Avoid “legacy/weak” intermediary names like `AccountCustomEntity` (and avoid unnecessary wrapper columns like `IPCustomEntity`) when a direct standard field already exists.

Apply this consistently:
- **Account entities:** If you have a UPN, map `FullName` to the UPN-derived field (commonly `UserPrincipalName`) rather than a legacy `*CustomEntity` column.
- **IP entities:** Prefer mapping from the actual IP source field (e.g., `SrcIpAddr`) directly instead of creating an `IPCustomEntity` wrapper just to rename.
- **If the platform expects split identifiers:** follow the documented entity model (e.g., Name vs UPN suffix) instead of relying on a legacy “FullName” mapping.

Example (replace legacy mapping):
```kusto
// Before (legacy/weak naming)
| extend AccountCustomEntity = UserPrincipalName
...
entityMappings:
  - entityType: Account
    fieldMappings:
      - identifier: FullName
        columnName: AccountCustomEntity

// After (standard identifier)
| extend UserPrincipalName = tostring(InitiatedBy.user.userPrincipalName)
...
entityMappings:
  - entityType: Account
    fieldMappings:
      - identifier: FullName
        columnName: UserPrincipalName
```

Example (avoid IP wrapper):
```kusto
// Before
| extend IPCustomEntity = SrcIpAddr
...
entityMappings:
  - entityType: Ip
    fieldMappings:
      - identifier: Address
        columnName: IPCustomEntity

// After
...
entityMappings:
  - entityType: Ip
    fieldMappings:
      - identifier: Address
        columnName: SrcIpAddr
```