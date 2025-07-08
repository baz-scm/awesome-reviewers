---
title: Centralize configuration values
description: Configuration values should be defined once and referenced throughout
  your project to ensure consistency and simplify maintenance. Hardcoded values scattered
  across multiple files lead to update errors and inconsistent configurations.
repository: Azure/azure-sdk-for-net
label: Configurations
language: Other
comments_count: 5
repository_stars: 5809
---

Configuration values should be defined once and referenced throughout your project to ensure consistency and simplify maintenance. Hardcoded values scattered across multiple files lead to update errors and inconsistent configurations.

For package versions, use MSBuild properties:
```xml
<!-- In Directory.Build.props or Packages.Data.props -->
<PropertyGroup>
  <AutoRestCSharpVersion>3.0.0-beta.20250701.1</AutoRestCSharpVersion>
</PropertyGroup>

<!-- Then reference it -->
<PackageReference Update="Microsoft.Azure.AutoRest.CSharp" Version="$(AutoRestCSharpVersion)" PrivateAssets="All" />
```

For framework targets, define a central property:
```xml
<!-- In Directory.Build.props -->
<PropertyGroup>
  <LtsTargetFramework>net8.0</LtsTargetFramework>
</PropertyGroup>

<!-- Then reference it in projects -->
<TargetFramework>$(LtsTargetFramework)</TargetFramework>
```

For script endpoints or configuration values, use shared variables:
```powershell
# Define once at the top of the script file
$ApiViewEndpointUrl = "https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges"

# Use throughout the script
function Create-API-Review {
  param (
    [string]$apiviewEndpoint = $ApiViewEndpointUrl,
    # ...
  )
}
```

This approach reduces the risk of inconsistencies when updates are needed, makes your build more reliable, and clearly communicates the relationships between dependent configuration values.
