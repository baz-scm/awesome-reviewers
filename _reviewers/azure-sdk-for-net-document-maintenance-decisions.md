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
