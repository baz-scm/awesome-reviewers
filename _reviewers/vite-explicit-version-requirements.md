---
title: Explicit version requirements
description: Always specify explicit Node.js version requirements in configuration
  files to ensure compatibility with language features and APIs. When updating supported
  versions, verify feature compatibility and document reasoning behind version constraints.
repository: vitejs/vite
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 74031
---

Always specify explicit Node.js version requirements in configuration files to ensure compatibility with language features and APIs. When updating supported versions, verify feature compatibility and document reasoning behind version constraints.

For example, when using ESM modules with require:
```js
// In eslint.config.js or other config files
settings: {
  node: {
    // Specify exact version ranges that support needed features
    version: '^20.19.0 || ^22.12.0+', // Required for require(ESM) support
  },
}
```

When changing version requirements, consider:
1. Feature support across different versions (like ESM support)
2. Breaking changes that might affect existing functionality
3. Development environment consistency across the team

Explicitly defined version requirements help prevent unexpected lint errors, runtime issues, and improve developer experience by documenting version-specific feature availability.