---
title: Approve AI dependencies conditionally
description: All AI-related dependencies (Microsoft.Extensions.AI.*, etc.) require
  explicit approval before inclusion and must be restricted to specific packages using
  conditional blocks in Packages.Data.props. Prefer version 8.x dependencies when
  available, and document any exceptions (such as using 9.x) with clear comments explaining
  the approval scope and reasoning.
repository: Azure/azure-sdk-for-net
label: AI
language: Other
comments_count: 2
repository_stars: 5809
---

All AI-related dependencies (Microsoft.Extensions.AI.*, etc.) require explicit approval before inclusion and must be restricted to specific packages using conditional blocks in Packages.Data.props. Prefer version 8.x dependencies when available, and document any exceptions (such as using 9.x) with clear comments explaining the approval scope and reasoning.

```xml
<!-- Example of properly documented and conditionally included AI dependency -->
<PackageReference Update="Microsoft.Extensions.AI" Version="9.5.0" /> <!-- 9.x approved for test project use, as there is no 8.x version available. -->

<!-- Example of conditional block to restrict an AI dependency to specific package -->
<ItemGroup Condition="'$(IsAIInferenceProject)' == 'true'">
  <PackageReference Update="Microsoft.Extensions.AI.Abstractions" Version="9.6.0"/>
</ItemGroup>
```
