---
title: Package dependency configuration
description: Configure dependencies appropriately in package.json based on usage patterns
  and requirements. This improves package maintainability, flexibility, and reduces
  unnecessary dependencies.
repository: nestjs/nest
label: Configurations
language: Json
comments_count: 4
repository_stars: 71767
---

Configure dependencies appropriately in package.json based on usage patterns and requirements. This improves package maintainability, flexibility, and reduces unnecessary dependencies.

- Use `peerDependencies` instead of direct dependencies for libraries that are loaded lazily or optionally used
- Add `peerDependenciesMeta` to mark peer dependencies as optional when appropriate
- Use flexible version ranges for stable libraries (e.g., `">=0.18"` or `"^0.18.0 || ^0.19.0"`)
- Avoid redundant type packages when libraries include their own TypeScript definitions

Example:
```json
{
  "dependencies": {
    "required-package": "2.3.1"
  },
  "peerDependencies": {
    "lazily-loaded-package": "^2.0.0",
    "optional-package": ">=1.0.0"
  },
  "peerDependenciesMeta": {
    "optional-package": {
      "optional": true
    }
  }
}
```

This approach ensures that your package properly declares its requirements while maintaining flexibility and avoiding unnecessary dependencies.