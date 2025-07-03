---
title: Address not mask
description: Always address the root cause of CI/CD pipeline issues rather than masking
  them with quick fixes. This applies to encoding problems, build failures, and other
  CI-related issues.
repository: Azure/azure-sdk-for-net
label: CI/CD
language: Other
comments_count: 2
repository_stars: 5809
---

Always address the root cause of CI/CD pipeline issues rather than masking them with quick fixes. This applies to encoding problems, build failures, and other CI-related issues.

Examples:
1. Remove BOM characters that cause encoding issues:
```diff
-﻿<Project Sdk="Microsoft.NET.Sdk">
+<Project Sdk="Microsoft.NET.Sdk">
```

2. Don't remove configuration that causes build failures - fix the underlying issue instead:
```diff
  <PropertyGroup>
    <Version>1.2.0-beta.1</Version>
+   <!--The ApiCompatVersion is managed automatically and should not generally be modified manually.-->
+   <ApiCompatVersion>1.1.2</ApiCompatVersion>
  </PropertyGroup>
```

When CI/CD pipelines fail, investigate the root cause rather than making superficial changes that only hide the problem. This ensures that real issues are properly addressed, maintaining the integrity and reliability of your build and deployment processes.
