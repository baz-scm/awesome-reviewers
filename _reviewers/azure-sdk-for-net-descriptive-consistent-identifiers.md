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


[
  {
    "discussion_id": "2164984072",
    "pr_number": 50844,
    "pr_file": "eng/common/mcp/azure-sdk-mcp.ps1",
    "created_at": "2025-06-24T21:52:22+00:00",
    "commented_code": "}\n    $vscodeConfig.servers = $orderedServers\n    Write-Host \"Updating vscode mcp config at $vscodeConfigPath\"\n    $vscodeConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $vscodeConfig -Force\n    $vscodeConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $vscodeConfigPath -Force",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2164984072",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50844,
        "pr_file": "eng/common/mcp/azure-sdk-mcp.ps1",
        "discussion_id": "2164984072",
        "commented_code": "@@ -51,7 +51,7 @@ if ($UpdateVsCodeConfig) {\n     }\n     $vscodeConfig.servers = $orderedServers\n     Write-Host \"Updating vscode mcp config at $vscodeConfigPath\"\n-    $vscodeConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $vscodeConfig -Force\n+    $vscodeConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $vscodeConfigPath -Force",
        "comment_created_at": "2025-06-24T21:52:22+00:00",
        "comment_author": "Copilot",
        "comment_body": "Fixed the variable used in the Set-Content command to correctly reference $vscodeConfigPath instead of $vscodeConfig, ensuring the updated VSCode configuration is written to the proper file path.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2143555839",
    "pr_number": 50576,
    "pr_file": "eng/Directory.Build.Common.targets",
    "created_at": "2025-06-12T19:58:02+00:00",
    "commented_code": "<PackageReference Remove=\"System.Text.Json\" />\n    <PackageReference Remove=\"System.Threading.Channels\" />\n    <PackageReference Remove=\"System.Threading.Tasks.Extensions\" />\n    <PackageReferences Remove=\"System.Memory\" />",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2143555839",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50576,
        "pr_file": "eng/Directory.Build.Common.targets",
        "discussion_id": "2143555839",
        "commented_code": "@@ -111,6 +111,7 @@\n     <PackageReference Remove=\"System.Text.Json\" />\n     <PackageReference Remove=\"System.Threading.Channels\" />\n     <PackageReference Remove=\"System.Threading.Tasks.Extensions\" />\n+    <PackageReferences Remove=\"System.Memory\" />",
        "comment_created_at": "2025-06-12T19:58:02+00:00",
        "comment_author": "Copilot",
        "comment_body": "The added element uses 'PackageReferences' (plural) instead of the consistent 'PackageReference' (singular) used in the surrounding lines, which could prevent the package from being removed as intended. Please update the tag to '<PackageReference Remove=\"System.Memory\" />'.\n```suggestion\n    <PackageReference Remove=\"System.Memory\" />\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2141327303",
    "pr_number": 50565,
    "pr_file": "eng/common/scripts/Invoke-GitHubAPI.ps1",
    "created_at": "2025-06-12T00:59:21+00:00",
    "commented_code": "[ValidateNotNullOrEmpty()]\n    [Parameter(Mandatory = $true)]\n    $CommitHash,\n    $State=\"open\"\n    $State=\"open\",\n    $AuthToken\n  )\n  $uri = \"https://api.github.com/search/issues?q=sha:$CommitHash+state:$State\"\n\n  return Invoke-RestMethod `\n          -Method GET `\n          -Uri $uri `\n          -MaximumRetryCount 3\n  $params = @{\n    Method = 'GET'\n    Uri = $uri\n    MaximumRetryCount = 3\n  }\n  if ($AuthToken) {\n    $params.Headers = Get-GitHubApiHeaders -token $AuthToken\n  }\n  return Invoke-RestMethod @params",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2141327303",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50565,
        "pr_file": "eng/common/scripts/Invoke-GitHubAPI.ps1",
        "discussion_id": "2141327303",
        "commented_code": "@@ -560,12 +560,17 @@ function Search-GitHubIssues {\n     [ValidateNotNullOrEmpty()]\n     [Parameter(Mandatory = $true)]\n     $CommitHash,\n-    $State=\"open\"\n+    $State=\"open\",\n+    $AuthToken\n   )\n   $uri = \"https://api.github.com/search/issues?q=sha:$CommitHash+state:$State\"\n-\n-  return Invoke-RestMethod `\n-          -Method GET `\n-          -Uri $uri `\n-          -MaximumRetryCount 3\n+  $params = @{\n+    Method = 'GET'\n+    Uri = $uri\n+    MaximumRetryCount = 3\n+  }\n+  if ($AuthToken) {\n+    $params.Headers = Get-GitHubApiHeaders -token $AuthToken\n+  }\n+  return Invoke-RestMethod @params",
        "comment_created_at": "2025-06-12T00:59:21+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider renaming the '$params' variable to something more descriptive (e.g. $invokeParams) to avoid potential confusion with any built-in parameter variables and to improve code clarity.\n```suggestion\n  $invokeParams = @{\n    Method = 'GET'\n    Uri = $uri\n    MaximumRetryCount = 3\n  }\n  if ($AuthToken) {\n    $invokeParams.Headers = Get-GitHubApiHeaders -token $AuthToken\n  }\n  return Invoke-RestMethod @invokeParams\n```",
        "pr_file_module": null
      }
    ]
  }
]
