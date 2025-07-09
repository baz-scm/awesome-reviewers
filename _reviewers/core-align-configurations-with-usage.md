---
title: Align configurations with usage
description: 'Configuration files should accurately reflect the actual requirements
  and characteristics of your codebase. When setting up TypeScript configurations:'
repository: vuejs/core
label: Configurations
language: Json
comments_count: 2
repository_stars: 50769
---

Configuration files should accurately reflect the actual requirements and characteristics of your codebase. When setting up TypeScript configurations:

1. **Match language settings to feature usage**: Ensure settings like `target` and `lib` correctly align with the ECMAScript features your code actually uses.

```json
// Good: Correctly specified to support Array.prototype.includes
{
  "compilerOptions": {
    "target": "es2015",
    "lib": ["es2016", "dom"]
  }
}

// Bad: Using inconsistent or inappropriate settings
{
  "compilerOptions": {
    "target": "es2015",
    "lib": ["esnext", "dom"] // Too broad, or "es2015" would be too restrictive
  }
}
```

2. **Create modular configurations**: Maintain separate configuration files for different parts of the project instead of overloading a single configuration file. This provides better control over component-specific settings.

For example, consider creating a separate tsconfig for private packages rather than adding them to the root configuration's include paths.