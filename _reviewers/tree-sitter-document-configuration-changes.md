---
title: Document configuration changes
description: When modifying configuration files (tsconfig.json, environment configs,
  build settings, etc.), always provide clear explanations for why the changes are
  necessary, what benefits they provide, and any potential impacts. Configuration
  changes can significantly affect build processes, development workflows, and application
  behavior, so reviewers and future...
repository: tree-sitter/tree-sitter
label: Configurations
language: Json
comments_count: 2
repository_stars: 21799
---

When modifying configuration files (tsconfig.json, environment configs, build settings, etc.), always provide clear explanations for why the changes are necessary, what benefits they provide, and any potential impacts. Configuration changes can significantly affect build processes, development workflows, and application behavior, so reviewers and future maintainers need to understand the reasoning behind modifications.

Include explanations either in:
- Pull request descriptions
- Inline comments within the configuration file
- Commit messages with detailed reasoning

Example from TypeScript configuration:
```json
{
  "compilerOptions": {
    // Enable composite mode for faster incremental builds with tsc --build
    "composite": true,
    // Ensure each file can be transpiled independently for bundlers like esbuild
    "isolatedModules": true
  },
  "include": [
    "src/**/*",
    // Include lib directory to ensure web-tree-sitter.d.ts is type-checked during builds
    "lib/**/*.ts"
  ]
}
```

This practice helps prevent confusion during code reviews and provides valuable context for future configuration maintenance.