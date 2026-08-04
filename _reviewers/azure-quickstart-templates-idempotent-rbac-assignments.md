---
title: Idempotent RBAC Assignments
description: 'When using Bicep to assign Azure RBAC roles, make roleAssignments deterministic
  and correct by:


  - Use the target principal’s **principalId** (e.g., managed identity principalId)
  rather than resourceId, and include it in the roleAssignment name seed.'
repository: Azure/azure-quickstart-templates
label: Security
language: Other
comments_count: 9
repository_stars: 14846
---

When using Bicep to assign Azure RBAC roles, make roleAssignments deterministic and correct by:

- Use the target principal’s **principalId** (e.g., managed identity principalId) rather than resourceId, and include it in the roleAssignment name seed.
- Compute the roleAssignment name as **guid(principalId, roleDefinitionId, scopeId)** so repeated deployments are idempotent.
- Set **roleDefinitionId** from an **existing roleDefinitions** resource’s `.id` (avoid brittle string concatenation).
- Specify **principalType** when required (e.g., ServicePrincipal).
- Prefer reasonable scoping for templates (don’t over-granularly narrow scope unless there’s a strong need), but keep scopes explicit.
- If deployments are intermittently failing right after RBAC changes, add a small **RBAC propagation wait**.

Example pattern:
```bicep
resource roleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  scope: subscription()
  name: '43d0d8ad-25c7-4714-9337-8ba259a9fe05' // role definition GUID
}

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(managedIdentity.properties.principalId, roleDefinition.id, resourceGroup().id)
  scope: resourceGroup() // make scope explicit
  properties: {
    roleDefinitionId: roleDefinition.id
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
```

Apply this consistently anywhere you create roleAssignments (storage, Key Vault, Digital Twins, etc.) to prevent duplicate/conflicting assignments and reduce deployment flakiness.