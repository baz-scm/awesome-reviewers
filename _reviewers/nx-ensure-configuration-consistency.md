---
title: Ensure configuration consistency
description: Configuration files should maintain consistency in patterns, use correct
  paths and values, and follow established conventions across the codebase. This includes
  proper output paths, consistent dependency versioning patterns, and appropriate
  dependency categorization.
repository: nrwl/nx
label: Configurations
language: Json
comments_count: 4
repository_stars: 27518
---

Configuration files should maintain consistency in patterns, use correct paths and values, and follow established conventions across the codebase. This includes proper output paths, consistent dependency versioning patterns, and appropriate dependency categorization.

Key areas to verify:
- **Output paths**: Use correct directory structures (e.g., `dist/lib` instead of `{projectRoot}/src/lib`)
- **Dependency versioning**: Maintain consistent patterns within the same configuration scope (e.g., if using caret `^` for similar packages, apply it consistently)
- **Dependency categorization**: Place dependencies in appropriate sections (`dependencies` vs `devDependencies`)
- **Version alignment**: Check for potential conflicts with other changes and align with ecosystem standards when possible

Example from package.json:
```json
{
  "dependencies": {
    "@module-federation/enhanced": "^0.17.0",  // Keep caret for consistency
    "@module-federation/sdk": "^0.17.0"
  },
  "devDependencies": {
    "@nx/cypress": "workspace:*"  // Move dev-only deps here
  }
}
```