---
title: dependency classification standards
description: 'Ensure proper classification and versioning of package dependencies
  in package.json files. Dependencies should be classified based on their usage pattern:
  use regular `dependencies` for hard requirements that the package cannot function
  without, and `peerDependencies` for packages that consumers are expected to provide.
  When specifying version ranges, use...'
repository: prisma/prisma
label: Configurations
language: Json
comments_count: 8
repository_stars: 42967
---

Ensure proper classification and versioning of package dependencies in package.json files. Dependencies should be classified based on their usage pattern: use regular `dependencies` for hard requirements that the package cannot function without, and `peerDependencies` for packages that consumers are expected to provide. When specifying version ranges, use appropriate semantic versioning operators - prefer `>=` over `>` for minimum versions, and understand that v0.x packages behave differently than v1+ packages in semver.

For example, database drivers should typically be regular dependencies rather than peer dependencies:
```json
{
  "dependencies": {
    "@libsql/client": "0.8.0"
  }
}
```

For TypeScript requirements, specify minimum versions clearly:
```json
{
  "peerDependencies": {
    "typescript": ">=5.1.0"
  }
}
```

Remove unused dependencies to keep the dependency tree clean and avoid unnecessary bloat. When working with v0.x packages, be explicit about version ranges since `^0.48` won't match `0.49.1`, unlike v1+ packages.