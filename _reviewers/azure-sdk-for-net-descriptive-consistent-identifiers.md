---
title: Descriptive consistent identifiers
description: Use clear, descriptive identifiers that accurately reflect their purpose,
  and maintain consistent naming patterns throughout the codebase. This applies to
  variables, parameters, methods, and configuration elements.
repository: Azure/azure-sdk-for-net
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 5809
---

Use clear, descriptive identifiers that accurately reflect their purpose, and maintain consistent naming patterns throughout the codebase. This applies to variables, parameters, methods, and configuration elements.

For variables:
- Choose names that convey the variable's specific role and content
- Avoid generic names like `$params` in favor of more specific names like `$invokeParams`
- Ensure variable names match their intended usage to prevent errors

For configuration elements:
- Maintain consistent patterns (singular/plural forms, prefixes/suffixes)
- Follow established conventions already present in surrounding code

Example of improved variable naming:
```powershell
# Poor naming - generic and potentially confusing
$params = @{
  Method = 'GET'
  Uri = $uri
}
return Invoke-RestMethod @params

# Better naming - clearly indicates purpose
$invokeParams = @{
  Method = 'GET'
  Uri = $uri
}
return Invoke-RestMethod @invokeParams
```

Example of consistent naming in configuration:
```xml
<!-- Inconsistent naming pattern -->
<PackageReference Remove="System.Text.Json" />
<PackageReference Remove="System.Threading.Tasks.Extensions" />
<PackageReferences Remove="System.Memory" />

<!-- Consistent naming pattern -->
<PackageReference Remove="System.Text.Json" />
<PackageReference Remove="System.Threading.Tasks.Extensions" />
<PackageReference Remove="System.Memory" />
```

Descriptive and consistent naming reduces cognitive load for readers, prevents errors from misused variables, and makes the codebase more maintainable.
