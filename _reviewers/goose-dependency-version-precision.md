---
title: dependency version precision
description: Choose appropriate version constraints in package.json based on stability
  requirements and risk tolerance. Use tilde (~) for patch-level updates when you
  want stability but need bug fixes, caret (^) for minor updates when you can tolerate
  feature additions, or exact versions for maximum control. For critical dependencies
  requiring precise version control,...
repository: block/goose
label: Configurations
language: Json
comments_count: 2
repository_stars: 19037
---

Choose appropriate version constraints in package.json based on stability requirements and risk tolerance. Use tilde (~) for patch-level updates when you want stability but need bug fixes, caret (^) for minor updates when you can tolerate feature additions, or exact versions for maximum control. For critical dependencies requiring precise version control, consider using npm overrides to enforce specific versions across the dependency tree.

Example:
```json
{
  "dependencies": {
    "@mcp-ui/client": "~5.3.1"  // Allow patches only
  },
  "overrides": {
    "@mcp-ui/client": "5.3.1"   // Force exact version if needed
  }
}
```

The choice between "~5.3.1" (patches allowed) versus "5.3.1" (exact) should reflect your project's stability needs and tolerance for automatic updates.