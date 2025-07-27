---
title: Pin dependency versions
description: Always pin dependencies to exact versions in package.json instead of
  using semantic version ranges (^, ~) to ensure reproducible builds and prevent unintentional
  version drift during deployments.
repository: snyk/cli
label: Configurations
language: Json
comments_count: 6
repository_stars: 5178
---

Always pin dependencies to exact versions in package.json instead of using semantic version ranges (^, ~) to ensure reproducible builds and prevent unintentional version drift during deployments.

This practice is especially critical for applications deployed as units, where consistency across all dependency versions is essential. Using exact versions prevents scenarios where different environments might resolve to different dependency versions, leading to inconsistent behavior.

Use npm's `--save-exact` flag when installing dependencies:

```bash
# Instead of: npm install some-package
npm install some-package --save-exact

# Or use the shorthand:
npm install some-package -E
```

This will add the dependency to package.json without version range operators:

```json
{
  "dependencies": {
    "snyk-gradle-plugin": "4.1.0",  // ✅ Exact version
    "snyk-cpp-plugin": "2.24.0"     // ✅ Exact version
  }
}
```

Rather than:

```json
{
  "dependencies": {
    "snyk-gradle-plugin": "^4.1.0",  // ❌ Range allows 4.x.x
    "snyk-cpp-plugin": "^2.24.0"     // ❌ Range allows 2.x.x
  }
}
```

While package-lock.json provides some protection against version drift, pinning to exact versions in package.json provides an additional layer of certainty and makes dependency management intentions explicit to all team members.