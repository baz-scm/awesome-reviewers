---
title: Use Stable API Versions
description: When defining or calling APIs (including Azure Sentinel/Microsoft Security
  connector artifacts), always use a stable, supported `apiVersion` and keep it consistent
  across all related files. Avoid “preview”/older `apiVersion` values unless there
  is an explicit, documented need.
repository: Azure/Azure-Sentinel
label: API
language: Json
comments_count: 11
repository_stars: 6042
---

When defining or calling APIs (including Azure Sentinel/Microsoft Security connector artifacts), always use a stable, supported `apiVersion` and keep it consistent across all related files. Avoid “preview”/older `apiVersion` values unless there is an explicit, documented need.

How to apply:
- Upgrade preview/obsolete `apiVersion` fields in every related artifact (e.g., connector definition, polling config, DCR, and table resources) rather than only one file.
- Keep connector “kind”/feature usage compatible with the chosen API version.
- If a newer feature appears tied to a newer API release, either:
  - upgrade `apiVersion` to a stable version that supports it, or
  - revert the feature change to maintain compatibility with the currently supported API version.

Example (before/after):
```json
// Before (preview/older)
{
  "apiVersion": "2022-09-01-preview",
  "type": "Microsoft.SecurityInsights/dataConnectorDefinitions"
}
```
```json
// After (stable)
{
  "apiVersion": "2023-09-01",
  "type": "Microsoft.SecurityInsights/dataConnectorDefinitions"
}
```

Team standard:
- Default to the latest stable `apiVersion` for each resource type.
- Block PRs that introduce preview/older `apiVersion` values without an approved exception.