---
title: Use exact dependency versions
description: Always specify exact dependency versions in package.json files instead
  of using version ranges (^, ~) to ensure reproducible builds and prevent accidental
  upgrades that could introduce breaking changes.
repository: cypress-io/cypress
label: Configurations
language: Json
comments_count: 3
repository_stars: 48850
---

Always specify exact dependency versions in package.json files instead of using version ranges (^, ~) to ensure reproducible builds and prevent accidental upgrades that could introduce breaking changes.

When adding new dependencies or updating existing ones, pin to specific versions to maintain build consistency across environments. This is especially important for production applications where unexpected dependency updates could cause runtime issues.

Example:
```json
// ❌ Avoid version ranges
"dependencies": {
  "snap-shot-core": "^7.4.0",
  "diff": "^4.0.1"
}

// ✅ Use exact versions
"dependencies": {
  "snap-shot-core": "7.4.0", 
  "diff": "4.0.1"
}
```

Remember that configuration changes may require additional dependencies - for example, enabling `"importHelpers": true` in tsconfig.json requires adding `tslib` as an exact dependency. Always verify that configuration changes don't introduce missing dependency requirements.