---
title: Native fetch over dependencies
description: Prefer Node.js native fetch API over external HTTP client libraries like
  `node-fetch` when the target Node.js version supports stable native functionality.
  While fetch is available from Node.js 18+, it's considered stable from version 21
  onwards.
repository: bytedance/UI-TARS-desktop
label: API
language: Json
comments_count: 2
repository_stars: 18021
---

Prefer Node.js native fetch API over external HTTP client libraries like `node-fetch` when the target Node.js version supports stable native functionality. While fetch is available from Node.js 18+, it's considered stable from version 21 onwards.

Before adding HTTP client dependencies, evaluate:
- Target Node.js version compatibility
- Native API stability requirements  
- Whether external dependencies provide necessary additional features

Example of unnecessary dependency:
```json
// Avoid when targeting Node.js >= 21
"dependencies": {
  "node-fetch": "3.3.2"  // Remove if native fetch suffices
}
```

This reduces bundle size, eliminates potential security vulnerabilities from external packages, and leverages platform-native optimizations. Only retain HTTP client libraries when they provide essential features not available in the native fetch API or when targeting older Node.js versions where native fetch is unstable.