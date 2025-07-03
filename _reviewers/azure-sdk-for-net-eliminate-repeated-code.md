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
