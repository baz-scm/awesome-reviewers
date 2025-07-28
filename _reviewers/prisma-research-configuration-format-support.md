---
title: Research configuration format support
description: When migrating configuration files to newer formats, research current
  ecosystem support before defaulting to compatibility layers. Many tools and plugins
  may already support modern formats even if documentation suggests otherwise.
repository: prisma/prisma
label: Configurations
language: Other
comments_count: 2
repository_stars: 42967
---

When migrating configuration files to newer formats, research current ecosystem support before defaulting to compatibility layers. Many tools and plugins may already support modern formats even if documentation suggests otherwise.

Before using compatibility shims like `@eslint/eslintrc`'s `FlatCompat`, check if your required plugins and parsers have native support for the new format. This prevents unnecessary dependencies and technical debt while ensuring you benefit from modern configuration features.

Example approach:
```javascript
// Instead of immediately using compatibility layer:
const { FlatCompat } = require('@eslint/eslintrc')
const compat = new FlatCompat({...})

// First research if plugins support new format:
// Check plugin documentation, GitHub issues, or compatibility matrices
// Many plugins like @typescript-eslint and eslint-plugin-prettier 
// already support ESLint v9 flat config natively

// Then use native configuration when possible:
module.exports = [
  {
    files: ['**/*.ts'],
    // Native flat config approach
  }
]
```

This approach reduces maintenance burden and ensures you're using the most current, supported configuration patterns rather than legacy compatibility workarounds.