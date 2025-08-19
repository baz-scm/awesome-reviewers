---
title: Document build configuration changes
description: When modifying build tool configurations, especially during migrations,
  provide detailed technical justification for each change. Document why specific
  options, plugins, or flags are being added, removed, or modified with concrete reasoning.
repository: microsoft/playwright
label: CI/CD
language: JavaScript
comments_count: 2
repository_stars: 76113
---

When modifying build tool configurations, especially during migrations, provide detailed technical justification for each change. Document why specific options, plugins, or flags are being added, removed, or modified with concrete reasoning.

This practice ensures build pipeline changes are transparent, maintainable, and can be properly reviewed. It prevents configuration drift and helps future developers understand the rationale behind build decisions.

Example of good documentation:
```javascript
// Remove babel plugins that are now redundant with esbuild:
// - "@babel/plugin-transform-logical-assignment-operators" - logical assignment 
//   has been natively supported since Node 15
// - "@babel/plugin-transform-nullish-coalescing-operator" - nullish coalescing 
//   has been natively supported since Node 14  
// - "@babel/plugin-transform-modules-commonjs" - handled by --format=cjs flag
args: [
  'esbuild',
  '--format=cjs',
  '--platform=node'
]
```

Always explain the technical basis for configuration decisions, reference version support when relevant, and note when options become obsolete due to dependency changes.