---
title: Config completeness and environment
description: Use deployment-time configuration (parameters/derived values) instead
  of hardcoded or partially-specified settings, and ensure env/config entries required
  for the selected feature/identity are fully present.
repository: Azure/azure-quickstart-templates
label: Configurations
language: Other
comments_count: 7
repository_stars: 14846
---

Use deployment-time configuration (parameters/derived values) instead of hardcoded or partially-specified settings, and ensure env/config entries required for the selected feature/identity are fully present.

Apply these checks:
- Derive environment/region from the deployment context (prefer `resourceGroup().location` and `environment().name`) rather than hardcoded regions or manual cloud selection.
- If a value is constrained by platform availability, encode it with `@allowed`/range validation (don’t rely on a fixed default that can break in other regions).
- Treat app settings / feature flags as fully wired configuration: when using user-assigned managed identities, include all required identity-related app settings (not just the account name).
- Parameterize behavior toggles (e.g., opt-in vs auto-correct) rather than embedding fixed behavior.
- Ensure configuration/script content is deterministic across build agents (e.g., normalize newlines for scripts/config files).

Example (function app managed identity storage auth app settings):
```bicep
param storageAccountName string
param userAssignedIdentityResourceId string

resource configAppSettings 'config' = {
  name: 'appsettings'
  properties: {
    AzureWebJobsStorage__accountName: storageAccountName
    AzureWebJobsStorage__clientId: userAssignedIdentityResourceId
    AzureWebJobsStorage__credential: 'ManagedIdentity'
  }
}
```
(Adjust the exact settings to match your runtime’s requirements; the key standard is “don’t omit identity-related env vars for the chosen auth mode.”)