---
title: Configure dependency management comprehensively
description: When configuring dependency management tools like Renovate, ensure comprehensive
  setup that includes modern syntax, strategic dependency grouping, and controlled
  update policies. Use current configuration formats (e.g., cron syntax instead of
  deprecated natural language), implement proper dependency grouping strategies, and
  configure update separation for...
repository: prometheus/prometheus
label: Configurations
language: Json
comments_count: 4
repository_stars: 59616
---

When configuring dependency management tools like Renovate, ensure comprehensive setup that includes modern syntax, strategic dependency grouping, and controlled update policies. Use current configuration formats (e.g., cron syntax instead of deprecated natural language), implement proper dependency grouping strategies, and configure update separation for better control.

Key practices:
- Use modern syntax formats: `"schedule": ["0 0-8 * * 1"], "timezone": "UTC"` instead of deprecated natural language
- Group related dependencies logically and consider excluding specific packages that shouldn't update individually
- Separate major/minor updates: `"separateMajorMinor": true, "separateMultipleMajor": true` to maintain compatibility control
- Extend management scope with custom regex managers to include dependencies referenced outside standard package files

Example configuration:
```json
{
  "schedule": ["0 0-8 * * 1"],
  "timezone": "UTC",
  "separateMajorMinor": true,
  "separateMultipleMajor": true,
  "packageRules": [
    {
      "description": "Group related UI dependencies",
      "matchPaths": ["web/ui/**"],
      "groupName": "UI Dependencies"
    }
  ]
}
```

This ensures dependency management is predictable, maintainable, and aligned with project requirements while leveraging the full capabilities of the tooling.