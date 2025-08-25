---
title: Externalize configuration values
description: Avoid hard-coding configuration values directly in source files. Instead,
  externalize them using environment variables, configuration files, or external resources.
  This improves maintainability, enables environment-specific settings, and reduces
  bundle sizes.
repository: bytedance/UI-TARS-desktop
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 18021
---

Avoid hard-coding configuration values directly in source files. Instead, externalize them using environment variables, configuration files, or external resources. This improves maintainability, enables environment-specific settings, and reduces bundle sizes.

For runtime configuration, use environment variables:
```typescript
// Instead of hard-coding:
id: 'ep-20250627155918-4jmhg'

// Use environment variables:
id: process.env.MODEL_ID
```

For build-time configuration, consider external dependencies:
```typescript
// Instead of bundling large resources:
const minifiedCSS = cleanCSS.minify(reportCSS).styles;

// Use external CDN resources in modern.config.js:
// https://unpkg.com/@ui-tars/visualizer/dist/report/
```

This approach enables different configurations per environment, reduces code coupling, and keeps sensitive or environment-specific values out of the codebase.