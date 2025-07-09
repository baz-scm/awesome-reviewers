---
title: Separate configuration responsibilities
description: Design configuration files with clear separation of responsibilities
  and maintain flexibility for future changes. Avoid unnecessarily bundling configurations
  together when they serve different purposes, as this can create tight coupling and
  make future transitions difficult.
repository: vitejs/vite
label: Configurations
language: Other
comments_count: 2
repository_stars: 74031
---

Design configuration files with clear separation of responsibilities and maintain flexibility for future changes. Avoid unnecessarily bundling configurations together when they serve different purposes, as this can create tight coupling and make future transitions difficult.

For tool-specific configurations (like babel, webpack, etc.), keep them in their dedicated files rather than abstracting them in framework plugins. This allows users to:
1. Have full visibility into their build pipeline
2. Customize configurations as needed
3. Swap underlying tools without major refactoring

When creating configuration patterns (like in renovate.json5, .gitignore, etc.), be as specific as possible when targeting special cases:

```json
// Instead of broad patterns like this:
{
  "fileMatch": ["\\.[mc]?[tj]sx?$"]
}

// Use specific targeting when appropriate:
{
  "fileMatch": ["packages\/create-vite\/src\/index\\.ts$"]
}
```

This approach reduces the risk of unintended matches and makes configurations more maintainable and transparent.