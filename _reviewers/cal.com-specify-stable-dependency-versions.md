---
title: Specify stable dependency versions
description: Always use specific semantic versions or caret ranges for stable releases
  in package.json and other dependency configuration files. Avoid using "latest" or
  development/pre-release versions as they can introduce unpredictable behavior and
  breaking changes that affect build reproducibility and team consistency.
repository: calcom/cal.com
label: Configurations
language: Json
comments_count: 2
repository_stars: 37732
---

Always use specific semantic versions or caret ranges for stable releases in package.json and other dependency configuration files. Avoid using "latest" or development/pre-release versions as they can introduce unpredictable behavior and breaking changes that affect build reproducibility and team consistency.

Use specific versions like:
```json
{
  "devDependencies": {
    "eslint-plugin-unused-imports": "^3.0.0",
    "@prisma/extension-optimize": "^1.0.1"
  }
}
```

Instead of:
```json
{
  "devDependencies": {
    "eslint-plugin-unused-imports": "latest",
    "@prisma/extension-optimize": "0.0.0-dev.202407222340"
  }
}
```

This practice ensures that all team members and CI/CD environments use the same dependency versions, preventing unexpected failures and maintaining consistent behavior across different development environments.