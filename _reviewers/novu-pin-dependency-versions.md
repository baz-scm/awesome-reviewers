---
title: Pin dependency versions
description: Always pin dependency versions by removing caret (^) and tilde (~) prefixes
  in package.json files to prevent build failures and ensure consistency across different
  environments and packages in a monorepo.
repository: novuhq/novu
label: Configurations
language: Json
comments_count: 2
repository_stars: 37700
---

Always pin dependency versions by removing caret (^) and tilde (~) prefixes in package.json files to prevent build failures and ensure consistency across different environments and packages in a monorepo.

Version ranges can cause unexpected issues when different packages resolve to different minor or patch versions of the same dependency, leading to build failures, API incompatibilities, or subtle runtime bugs. This is especially critical in monorepo setups where multiple packages may depend on the same library.

Example of problematic versioning:
```json
{
  "dependencies": {
    "react-icons": "^5.0.1",
    "@nestjs/common": "^10.4.1"
  }
}
```

Example of properly pinned versions:
```json
{
  "dependencies": {
    "react-icons": "5.0.1",
    "@nestjs/common": "10.4.1"
  }
}
```

For complex scenarios involving peer dependencies, leverage package manager features like PNPM overrides to ensure consistent version resolution across production and development environments.