---
title: Consistent module resolution
description: Configure consistent module resolution strategies across related projects
  and ensure package.json files are properly set up for the chosen strategy. Different
  strategies (Node10, NodeNext) have distinct behaviors regarding package.json handling,
  which can cause subtle resolution errors and confusing tracing output.
repository: microsoft/typescript
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 105378
---

Configure consistent module resolution strategies across related projects and ensure package.json files are properly set up for the chosen strategy. Different strategies (Node10, NodeNext) have distinct behaviors regarding package.json handling, which can cause subtle resolution errors and confusing tracing output.

For example, when using NodeNext:
```json
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "NodeNext",
    // Ensure traceResolution is consistently set across projects if needed for debugging
    "traceResolution": true
  }
}
```

And ensure your package.json correctly defines module entry points:
```json
// package.json
{
  "name": "my-package",
  "main": "build/index.js",  // Used by Node.js and some module resolution strategies
  "types": "build/index.d.ts" // Used by TypeScript to find type declarations
}
```

When troubleshooting module resolution issues, remember that inconsistent configuration can lead to unexpected behavior. If you need to trace module resolution, make sure the traceResolution option is set consistently across all relevant projects in your workspace.