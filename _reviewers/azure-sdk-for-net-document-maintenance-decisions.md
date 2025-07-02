---
title: Document maintenance decisions
description: 'Add clear documentation for any decisions that affect future code maintenance.
  This includes:


  1. Providing explanatory comments for non-obvious default values in parameters'
repository: Azure/azure-sdk-for-net
label: Documentation
language: Other
comments_count: 2
repository_stars: 5809
---

Add clear documentation for any decisions that affect future code maintenance. This includes:

1. Providing explanatory comments for non-obvious default values in parameters
2. Recording version updates in the CHANGELOG
3. Following established documentation structures and patterns

For example, when defining parameters with default values:

```powershell
[string]$RunDirectory = (Resolve-Path "${PSScriptRoot}/../../../"),  # Default points to repo root for consistent script execution
```

This documentation practice improves maintainability by ensuring that future developers understand the reasoning behind specific implementation choices, reducing the learning curve and helping to prevent unintended side effects during code modifications.


[
  {
    "discussion_id": "2100938237",
    "pr_number": 50187,
    "pr_file": "eng/common/mcp/azure-sdk-mcp.ps1",
    "created_at": "2025-05-21T18:39:58+00:00",
    "commented_code": "[string]$Version, # Default to latest\n    [string]$InstallDirectory = (Join-Path $HOME \".azure-sdk-mcp\" \"azsdk\"),\n    [string]$Repository = 'Azure/azure-sdk-tools',\n    [string]$RunDirectory = (Resolve-Path \"${PSScriptRoot}/../../../\"),",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2100938237",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50187,
        "pr_file": "eng/common/mcp/azure-sdk-mcp.ps1",
        "discussion_id": "2100938237",
        "commented_code": "@@ -6,6 +6,7 @@ param(\n     [string]$Version, # Default to latest\n     [string]$InstallDirectory = (Join-Path $HOME \".azure-sdk-mcp\" \"azsdk\"),\n     [string]$Repository = 'Azure/azure-sdk-tools',\n+    [string]$RunDirectory = (Resolve-Path \"${PSScriptRoot}/../../../\"),",
        "comment_created_at": "2025-05-21T18:39:58+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider adding a comment explaining the rationale behind the default value for RunDirectory to aid future maintainability.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2097186668",
    "pr_number": 50156,
    "pr_file": "eng/Packages.Data.props",
    "created_at": "2025-05-20T07:26:01+00:00",
    "commented_code": "All should have PrivateAssets=\"All\" set so they don't become package dependencies\n  -->\n  <ItemGroup>\n    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250515.1\" PrivateAssets=\"All\" />\n    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250519.1\" PrivateAssets=\"All\" />",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2097186668",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50156,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2097186668",
        "commented_code": "@@ -277,7 +277,7 @@\n     All should have PrivateAssets=\"All\" set so they don't become package dependencies\n   -->\n   <ItemGroup>\n-    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250515.1\" PrivateAssets=\"All\" />\n+    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250519.1\" PrivateAssets=\"All\" />",
        "comment_created_at": "2025-05-20T07:26:01+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider adding an entry in the CHANGELOG to reflect the AutoRest.CSharp version bump to 3.0.0-beta.20250519.1.",
        "pr_file_module": null
      }
    ]
  }
]
