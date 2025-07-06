---
title: Complete configuration fields
description: Ensure all plugin configuration files include the complete set of required
  fields specific to their plugin type. Missing configuration fields can cause unexpected
  behavior or failures when the plugin is used.
repository: grafana/grafana
label: Configurations
language: Json
comments_count: 3
repository_stars: 68825
---

Ensure all plugin configuration files include the complete set of required fields specific to their plugin type. Missing configuration fields can cause unexpected behavior or failures when the plugin is used.

For example, all decoupled data sources must include the "executable" field in their plugin.json:

```json
{
  "id": "your-datasource",
  "name": "Your Datasource",
  "type": "datasource",
  "executable": "gpx_your_datasource",
  // other configuration...
}
```

When structuring configuration keys in localization files, avoid duplicating namespace information that is already represented in the file path. Use clear and concise language in configuration documentation, especially for deprecation notices or important instructions.

Reference existing plugins of the same type to ensure consistency in configuration structure. This helps maintain uniformity across the codebase and ensures all necessary configurations are properly declared.