---
title: Infer Dependencies
description: When modeling Bicep resources, prefer symbolic references and proper
  parent/child wiring so ARM/Bicep can infer ordering automatically. This improves
  readability (fewer manual `dependsOn`/hand-built IDs) and reduces dependency bugs.
repository: Azure/azure-quickstart-templates
label: Code Style
language: Other
comments_count: 9
repository_stars: 14846
---

When modeling Bicep resources, prefer symbolic references and proper parent/child wiring so ARM/Bicep can infer ordering automatically. This improves readability (fewer manual `dependsOn`/hand-built IDs) and reduces dependency bugs.

Rules:
1) Use `.id` from declared resources (or `existing` resources) instead of recreating IDs with `resourceId()`/string concatenation.
2) Use `parent:` for child resources (e.g., `.../profiles/accessRules`) rather than manually building compound `name` strings.
3) Remove `dependsOn` when the resource already references another resource’s `.id` (or when `parent:` implies the dependency).
4) Use idiomatic Bicep expressions for readability (e.g., string interpolation over `concat()`), and keep a consistent file layout: `params` → `vars` → `resources` → `outputs`.

Example:
```bicep
resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: vnetName
  location: location
  properties: {
    subnets: [
      {
        name: 'aksSubnet'
        properties: {
          addressPrefix: aksSubnetPrefix
        }
      }
    ]
  }
}

// Prefer referencing the child resource id via a symbolic reference
resource supercomputer 'Microsoft.Discovery/supercomputers@2026-02-01-preview' = {
  name: supercomputerName
  location: location
  properties: {
    subnetId: resourceId(
      'Microsoft.Network/virtualNetworks/subnets',
      vnet.name,
      'aksSubnet'
    )
  }
  // No manual dependsOn when subnetId comes from the VNet modeling
}

// Child resources: use parent instead of composing names
resource profile 'Microsoft.Network/networkSecurityPerimeters/profiles@2023-07-01-preview' = {
  parent: networkSecurityPerimeter
  name: profileName
  location: location
}

resource inboundAccessRule 'Microsoft.Network/networkSecurityPerimeters/profiles/accessRules@2023-07-01-preview' = {
  parent: profile
  name: inboundIpv4AccessRuleName
  location: location
  properties: {}
}
```

Apply this consistently: if you add a manual `dependsOn`, ask whether a symbolic `.id`/`parent` reference would make it unnecessary.