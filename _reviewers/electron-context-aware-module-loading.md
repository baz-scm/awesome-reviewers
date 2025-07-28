---
title: Context-aware module loading
description: Choose appropriate module loading syntax based on your execution context
  and build configuration settings. Different environments have different module system
  capabilities that must be respected.
repository: electron/electron
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 117644
---

Choose appropriate module loading syntax based on your execution context and build configuration settings. Different environments have different module system capabilities that must be respected.

When `tsconfig.json` has `module: esnext` or `package.json` has `type: module`, import statements may not be automatically transformed to require calls. In contexts like sandboxed preload scripts that don't support ESM, you must use require syntax instead:

```typescript
// In sandboxed preload scripts, use require even with ESM config
const { ipcRenderer, contextBridge } = require('electron/renderer');

// For dynamic imports in ESM contexts, use import()
packageJson = await import(packageJsonPath, { assert: { type: 'json' } });
```

Always verify that your chosen loading mechanism is compatible with both your build configuration and the target execution environment. Sandboxed contexts, Node.js versions, and TypeScript compiler settings all influence which module syntax will work correctly.