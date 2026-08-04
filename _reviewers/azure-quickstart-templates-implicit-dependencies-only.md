---
title: Implicit Dependencies Only
description: 'For CI/CD stability and to avoid Bicep linter/build failures, do not
  add explicit `dependsOn` entries when Bicep can infer the dependency.


  **Rule**

  - **Remove unnecessary `dependsOn`** when the deployment order is already implied
  by:'
repository: Azure/azure-quickstart-templates
label: CI/CD
language: Other
comments_count: 5
repository_stars: 14846
---

For CI/CD stability and to avoid Bicep linter/build failures, do not add explicit `dependsOn` entries when Bicep can infer the dependency.

**Rule**
- **Remove unnecessary `dependsOn`** when the deployment order is already implied by:
  - referencing another resource/module’s **ID/name/properties** (including module `outputs`) in `params` or resource properties
  - using **parent/child resource syntax** (so ordering is structurally defined)
- **Keep or add `dependsOn` only when necessary** to handle ordering gaps that Bicep inference won’t cover (commonly: `Microsoft.Resources/deploymentScripts` or other runtime steps that require a resource to exist before the script runs).

**Why**
- CI often runs Bicep linting and treats warnings/errors as failures (e.g., `no-unnecessary-dependson`).

**Example (remove when outputs are referenced)**
```bicep
module aiDependencies 'modules/dependent-resources.bicep' = {
  name: 'dependencies'
  params: { location: location }
}

module aiResource 'modules/ai-resource.bicep' = {
  name: 'ai'
  params: {
    keyVaultId: aiDependencies.outputs.keyvaultId
    storageAccountId: aiDependencies.outputs.storageId
  }
  // dependsOn: [ aiDependencies ]  // unnecessary; parameter references already imply it
}
```

**Example (keep when a runtime script needs prior resources)**
```bicep
resource deploymentScript 'Microsoft.Resources/deploymentScripts@2020-10-01' = {
  name: 'upload'
  // Ensure the script runs only after required storage/container are available
  dependsOn: [ storage ]
  properties: { /* scriptContent */ }
}
```

Apply this standard consistently so templates pass linting in pipelines and deployments remain deterministic.