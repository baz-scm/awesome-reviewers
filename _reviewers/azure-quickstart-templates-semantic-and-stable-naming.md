---
title: Semantic And Stable Naming
description: 'Use names that clearly convey intent, keep them consistent across related
  resources, and ensure deterministic uniqueness.


  **1) Make names/intents self-explanatory**'
repository: Azure/azure-quickstart-templates
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 14846
---

Use names that clearly convey intent, keep them consistent across related resources, and ensure deterministic uniqueness.

**1) Make names/intents self-explanatory**
- Prefer descriptive `displayName` (especially for customer attachment points), e.g. “Database (attach CosmosDB here)”.

**2) Avoid naming drift by reusing identifiers**
- When one resource depends on another being named a certain way (e.g., discovery rules anchored to an entity), reference the actual identifier instead of re-stating the same literal.

```bicep
resource computeEntity 'Microsoft.CloudHealth/healthmodels/entities@2026-05-01-preview' = {
  parent: healthModel
  name: 'compute'
  properties: {
    displayName: 'Compute'
  }
}

resource rootToCompute 'Microsoft.CloudHealth/healthmodels/relationships@2026-05-01-preview' = {
  parent: healthModel
  name: '${healthModelName}-compute'
  properties: {
    parentEntityName: healthModelName
    childEntityName: computeEntity.name // reuse, don’t duplicate literals
  }
}

resource discoveryRule 'Microsoft.CloudHealth/healthmodels/discoveryrules@2026-05-01-preview' = {
  parent: healthModel
  name: computeEntity.name // keeps discovery anchored if entity naming changes
  properties: {
    // ...
  }
}
```

**3) Prefer speaking names over opaque GUIDs (when possible)**
- For relationship/discovery resource `name` values, use readable patterns like `${parent.name}-${child.name}`.

```bicep
name: '${parentEntityName}-${childEntityName}'
```

**4) Use deterministic uniqueness for global names**
- When a name must be globally unique, use `uniqueString` with stable seeds (e.g., `resourceGroup().id`) rather than `utcNow()`/time-based values.

```bicep
param instanceName string = 'app-${uniqueString(resourceGroup().id)}'
```

Applying these rules improves clarity (what the entity is for), reduces broken wiring due to drift, and prevents nondeterministic deployment diffs.