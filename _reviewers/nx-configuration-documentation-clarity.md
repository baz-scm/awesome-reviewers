---
title: Configuration documentation clarity
description: 'Configuration changes and examples should be documented with clear formatting,
  proper context, and helpful references to aid developer understanding.

  '
repository: nrwl/nx
label: Configurations
language: Other
comments_count: 4
repository_stars: 27518
---

Configuration changes and examples should be documented with clear formatting, proper context, and helpful references to aid developer understanding.

When documenting configuration changes:
- Add filename comments to code blocks to provide context
- Use diff blocks to clearly show before/after states for configuration migrations
- Include links to relevant reference documentation for configuration options
- Consolidate related configuration information rather than scattering it across multiple sections

Example of clear configuration documentation:

```diff
// nx.json
{
  "plugins": [
    {
      "plugin": "@nx/dotnet",
      "options": {
-       "inferredTargets": {
-         "build": "build",
-         "test": {
-           "targetName": "test:dotnet",
-           "cache": false
-         }
-       }
+       "build": {
+         "targetName": "build"
+       },
+       "test": {
+         "targetName": "test:dotnet"
+       }
      }
    }
  ]
}
```

This approach helps developers quickly understand what configuration files are being modified, what specific changes are needed, and where to find additional information about configuration options.