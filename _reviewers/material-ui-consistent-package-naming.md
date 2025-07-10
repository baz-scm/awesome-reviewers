---
title: Consistent package naming
description: Use consistent and meaningful naming patterns for packages based on their
  purpose, visibility, and scope. This improves clarity in build scripts, dependencies,
  and during development.
repository: mui/material-ui
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 96063
---

Use consistent and meaningful naming patterns for packages based on their purpose, visibility, and scope. This improves clarity in build scripts, dependencies, and during development.

For regular packages:
- Use descriptive names that clearly indicate the package's purpose or technology
- Example: `@app/pigment-css-next-app` instead of `@app/next-app`

For special-purpose packages:
- Apply consistent prefixes based on package visibility:
  - `@mui/internal-*` for internal packages used across the codebase
  - `@mui/private-*` for packages not intended for external consumption
  - `@mui/test-*` for testing utilities

In package.json:
```json
{
  "name": "@mui/internal-bundle-size",
  // or
  "name": "@app/pigment-css-next-app"
}
```

This naming consistency makes it easier to understand package purposes when referenced in scripts (e.g., `--ignore @app/pigment-css-next-app`) and helps developers immediately recognize the intended usage scope of each package.