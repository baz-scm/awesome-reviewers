---
title: Optimize CI type checking
description: Configure separate TypeScript type-checking strategies for CI environments
  and local development. CI pipelines should run complete type checks that validate
  the entire codebase, while local development can use faster configurations to improve
  developer productivity.
repository: vercel/ai
label: CI/CD
language: Json
comments_count: 2
repository_stars: 15590
---

Configure separate TypeScript type-checking strategies for CI environments and local development. CI pipelines should run complete type checks that validate the entire codebase, while local development can use faster configurations to improve developer productivity.

Example implementation:
```json
// package.json
{
  "scripts": {
    "type-check": "tsc --build",                       // Faster checks for local development
    "type-check:full": "tsc --build tsconfig.with-examples.json", // Comprehensive checks for CI
    "clean": "rimraf dist"                             // Add cleanup before builds
  }
}
```

In your CI pipeline configuration, always use the more thorough type checking:
```yaml
# CI configuration
steps:
  - name: Type Check
    run: npm run type-check:full
```

This approach ensures your CI pipeline catches all type errors while developers can work efficiently with faster feedback loops during local development. When changing build configurations, document the implications for the team and update CI pipelines accordingly.