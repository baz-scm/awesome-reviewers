---
title: Dependency version specification
description: Ensure proper dependency version specification and compatibility management
  in package.json files. Use explicit version ranges for peer dependencies to express
  compatibility constraints, avoid workspace references in examples and published
  packages, and properly classify dependencies based on usage patterns.
repository: TanStack/router
label: Configurations
language: Json
comments_count: 8
repository_stars: 11590
---

Ensure proper dependency version specification and compatibility management in package.json files. Use explicit version ranges for peer dependencies to express compatibility constraints, avoid workspace references in examples and published packages, and properly classify dependencies based on usage patterns.

Key practices:
- Use version ranges for peer dependencies to support multiple major versions: `"zod": "^3.25.0 || ^4.0.0"`
- Explicitly declare peer dependencies required by strict dependency managers like pnpm
- Replace workspace references with absolute versions in examples: use `"^1.46.3"` instead of `"workspace:^"`
- Add version constraints for peer dependencies: `"arktype": ">=2 <=3"`
- Avoid adding dependencies that are inherited from monorepo root (like vitest)
- Remove unused dependencies after verification they're not actually used
- Use absolute version numbers without workspace prefixes for external compatibility (codesandbox, etc.)

Example:
```json
{
  "peerDependencies": {
    "@tanstack/router-core": "^1.120.5",
    "zod": "^3.25.0 || ^4.0.0"
  },
  "devDependencies": {
    "@tanstack/react-router": "^1.46.3"
  }
}
```