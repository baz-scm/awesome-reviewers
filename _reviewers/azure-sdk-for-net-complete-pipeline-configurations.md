---
title: Complete pipeline configurations
description: Ensure all CI/CD configuration files have their required fields properly
  populated with specific values rather than empty strings or placeholders. Missing
  or incomplete configuration values can cause pipeline failures, prevent proper asset
  publishing, or create unnecessary maintenance overhead. Regularly review configurations
  to validate they're accurate...
repository: Azure/azure-sdk-for-net
label: CI/CD
language: Json
comments_count: 2
repository_stars: 5809
---

Ensure all CI/CD configuration files have their required fields properly populated with specific values rather than empty strings or placeholders. Missing or incomplete configuration values can cause pipeline failures, prevent proper asset publishing, or create unnecessary maintenance overhead. Regularly review configurations to validate they're accurate and still necessary.

**Example:**
```json
{
  "AssetsRepo": "Azure/azure-sdk-assets",
  "AssetsRepoPrefixPath": "net",
  "TagPrefix": "net/bicep/Azure.ResourceManager.Resources.Bicep",
  "Tag": "1.0.0"  // Always include specific version tags, not empty strings
}
```

When specifying environment resources such as VM images or test pools, ensure they reference valid, current resources and periodically evaluate if custom resources are still needed to avoid maintaining unnecessary infrastructure.
