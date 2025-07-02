---
title: Eliminate repeated code
description: Reduce code duplication by extracting repeated patterns into variables,
  loops, or helper functions. When you find yourself writing similar lines of code
  multiple times, refactor to a more DRY (Don't Repeat Yourself) approach to improve
  maintainability and readability.
repository: Azure/azure-sdk-for-net
label: Code Style
language: Other
comments_count: 2
repository_stars: 5809
---

Reduce code duplication by extracting repeated patterns into variables, loops, or helper functions. When you find yourself writing similar lines of code multiple times, refactor to a more DRY (Don't Repeat Yourself) approach to improve maintainability and readability.

Example 1 - Refactor repetitive logging:
```powershell
# Before
Write-Host "Configuration File: $ConfigPath"
Write-Host $rawConfig
Write-Host "SelectionType: $Selection"
Write-Host "DisplayNameFilter: $DisplayNameFilter"
Write-Host "Filters: $Filters"

# After
$logEntries = @{
    "Configuration File" = $ConfigPath
    "Raw Configuration" = $rawConfig
    "SelectionType" = $Selection
    "DisplayNameFilter" = $DisplayNameFilter
    "Filters" = $Filters
}
foreach ($key in $logEntries.Keys) {
    Write-Host "$key: $($logEntries[$key])"
}
```

Example 2 - Store nested paths in variables:
```powershell
# Before
if ($yml["options"]["@azure-tools/typespec-csharp"]["package-dir"]) {
    $packageDir = $yml["options"]["@azure-tools/typespec-csharp"]["package-dir"]
}
if ($yml["options"]["@azure-tools/typespec-csharp"]["service-dir"]) {
    $service = $yml["options"]["@azure-tools/typespec-csharp"]["service-dir"]
}

# After
$csharpOpts = $yml["options"]["@azure-tools/typespec-csharp"]
if ($csharpOpts["package-dir"]) {
    $packageDir = $csharpOpts["package-dir"]
}
if ($csharpOpts["service-dir"]) {
    $service = $csharpOpts["service-dir"]
}
```


[
  {
    "discussion_id": "2178653926",
    "pr_number": 50998,
    "pr_file": "eng/common/scripts/job-matrix/Create-JobMatrix.ps1",
    "created_at": "2025-07-01T22:33:14+00:00",
    "commented_code": ")\n\n. $PSScriptRoot/job-matrix-functions.ps1\n. $PSScriptRoot/../logging.ps1\n\nif (!(Test-Path $ConfigPath)) {\n    Write-Error \"ConfigPath '$ConfigPath' does not exist.\"\n    exit 1\n}\n$config = GetMatrixConfigFromFile (Get-Content $ConfigPath -Raw)\n$rawConfig = Get-Content $ConfigPath -Raw\n$config = GetMatrixConfigFromFile $rawConfig\n# Strip empty string filters in order to be able to use azure pipelines yaml join()\n$Filters = $Filters | Where-Object { $_ }\n\nLogGroupStart \"Matrix generation configuration\"\nWrite-Host \"Configuration File: $ConfigPath\"\nWrite-Host $rawConfig\nWrite-Host \"SelectionType: $Selection\"\nWrite-Host \"DisplayNameFilter: $DisplayNameFilter\"\nWrite-Host \"Filters: $Filters\"\nWrite-Host \"Replace: $Replace\"\nWrite-Host \"NonSparseParameters: $NonSparseParameters\"",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2178653926",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50998,
        "pr_file": "eng/common/scripts/job-matrix/Create-JobMatrix.ps1",
        "discussion_id": "2178653926",
        "commented_code": "@@ -21,15 +21,27 @@ param (\n )\n \n . $PSScriptRoot/job-matrix-functions.ps1\n+. $PSScriptRoot/../logging.ps1\n \n if (!(Test-Path $ConfigPath)) {\n     Write-Error \"ConfigPath '$ConfigPath' does not exist.\"\n     exit 1\n }\n-$config = GetMatrixConfigFromFile (Get-Content $ConfigPath -Raw)\n+$rawConfig = Get-Content $ConfigPath -Raw\n+$config = GetMatrixConfigFromFile $rawConfig\n # Strip empty string filters in order to be able to use azure pipelines yaml join()\n $Filters = $Filters | Where-Object { $_ }\n \n+LogGroupStart \"Matrix generation configuration\"\n+Write-Host \"Configuration File: $ConfigPath\"\n+Write-Host $rawConfig\n+Write-Host \"SelectionType: $Selection\"\n+Write-Host \"DisplayNameFilter: $DisplayNameFilter\"\n+Write-Host \"Filters: $Filters\"\n+Write-Host \"Replace: $Replace\"\n+Write-Host \"NonSparseParameters: $NonSparseParameters\"",
        "comment_created_at": "2025-07-01T22:33:14+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The sequence of Write-Host statements for logging could be refactored into a loop or helper function to reduce duplication and improve maintainability.\n```suggestion\n$logEntries = @{\n    \"Configuration File\" = $ConfigPath\n    \"Raw Configuration\" = $rawConfig\n    \"SelectionType\" = $Selection\n    \"DisplayNameFilter\" = $DisplayNameFilter\n    \"Filters\" = $Filters\n    \"Replace\" = $Replace\n    \"NonSparseParameters\" = $NonSparseParameters\n}\nforeach ($key in $logEntries.Keys) {\n    Write-Host \"$key: $($logEntries[$key])\"\n}\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176461585",
    "pr_number": 50970,
    "pr_file": "eng/scripts/automation/GenerateAndBuildLib.ps1",
    "created_at": "2025-07-01T05:30:04+00:00",
    "commented_code": "if ($yml[\"parameters\"] -And $yml[\"parameters\"][\"service-dir\"]) {\n            $service = $yml[\"parameters\"][\"service-dir\"][\"default\"];\n        }\n        if ($yml[\"options\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]) {\n            $packageDir = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]\n        if ($yml[\"options\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"]) {\n            if ($yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]) {\n                $packageDir = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]\n            }\n            if ($yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"service-dir\"]) {\n                $service = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"service-dir\"]",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2176461585",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50970,
        "pr_file": "eng/scripts/automation/GenerateAndBuildLib.ps1",
        "discussion_id": "2176461585",
        "commented_code": "@@ -917,8 +917,13 @@ function GetSDKProjectFolder()\n         if ($yml[\"parameters\"] -And $yml[\"parameters\"][\"service-dir\"]) {\n             $service = $yml[\"parameters\"][\"service-dir\"][\"default\"];\n         }\n-        if ($yml[\"options\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]) {\n-            $packageDir = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]\n+        if ($yml[\"options\"] -And $yml[\"options\"][\"@azure-tools/typespec-csharp\"]) {\n+            if ($yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]) {\n+                $packageDir = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"package-dir\"]\n+            }\n+            if ($yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"service-dir\"]) {\n+                $service = $yml[\"options\"][\"@azure-tools/typespec-csharp\"][\"service-dir\"]",
        "comment_created_at": "2025-07-01T05:30:04+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider assigning `$yml[\"options\"][\"@azure-tools/typespec-csharp\"]` to a local variable (e.g. `$csharpOpts`) to avoid repeated indexing and improve readability.\n```suggestion\n            $csharpOpts = $yml[\"options\"][\"@azure-tools/typespec-csharp\"]\n            if ($csharpOpts[\"package-dir\"]) {\n                $packageDir = $csharpOpts[\"package-dir\"]\n            }\n            if ($csharpOpts[\"service-dir\"]) {\n                $service = $csharpOpts[\"service-dir\"]\n```",
        "pr_file_module": null
      }
    ]
  }
]
