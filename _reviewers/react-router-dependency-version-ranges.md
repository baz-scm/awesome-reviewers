---
title: dependency version ranges
description: When configuring dependencies in package.json, use version ranges that
  maintain backwards compatibility and follow semantic versioning principles. For
  peer dependencies, prefer ranges that support multiple major versions when possible
  to avoid forcing consumers to upgrade unnecessarily.
repository: remix-run/react-router
label: Configurations
language: Json
comments_count: 5
repository_stars: 55270
---

When configuring dependencies in package.json, use version ranges that maintain backwards compatibility and follow semantic versioning principles. For peer dependencies, prefer ranges that support multiple major versions when possible to avoid forcing consumers to upgrade unnecessarily.

Key practices:
- Use `||` syntax for backwards-compatible peer dependencies: `"wrangler": "^3.28.2 || ^4.0.0"`
- Prefer broader version ranges over specific versions: `^4.0.0` instead of `^4.2.0` to support `4.0.x` and `4.1.x`
- In monorepo root package.json, dependencies can be placed in `dependencies` rather than `devDependencies` since end users never consume the root package
- Use version placeholders like `"*"` in templates that get replaced by build tools: `"react-router": "*"`
- Be pragmatic about pre-release versions when the usage is limited and well-tested, but document the reasoning

Example of proper peer dependency configuration:
```json
{
  "peerDependencies": {
    "typescript": "^5.1.0",
    "vite": "^5.1.0 || ^6.0.0",
    "wrangler": "^3.28.2 || ^4.0.0"
  }
}
```

This approach reduces dependency conflicts, improves compatibility, and makes packages more consumable across different project configurations.