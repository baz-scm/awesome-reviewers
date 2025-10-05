---
title: environment-aware API usage
description: Always detect the runtime environment before using environment-specific
  APIs or utilities. This is crucial for networking applications that may run in browsers,
  Node.js servers, or cross-platform contexts.
repository: TanStack/router
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 11590
---

Always detect the runtime environment before using environment-specific APIs or utilities. This is crucial for networking applications that may run in browsers, Node.js servers, or cross-platform contexts.

Key practices:
1. Use platform-specific utilities when available (e.g., `path.posix.join` for consistent path handling)
2. Check for environment-specific globals before accessing them (e.g., `typeof window !== 'undefined' && 'CSS' in window` before using `window.CSS.supports()`)
3. Use explicit module prefixes for built-in modules (e.g., `"node:url"` instead of `"url"` for Node.js built-ins)

Example of proper environment detection:
```typescript
// Check for browser environment before using browser APIs
if (!this.isServer && typeof window !== 'undefined' && 'CSS' in window) {
  this.isViewTransitionTypesSupported = window.CSS.supports(...)
}

// Use Node.js module prefix for built-in modules
import { fileURLToPath } from 'node:url'

// Use platform-specific path utilities
path.posix.join(routesDirectoryFromRoot, v.filePath as string)
```

This approach prevents runtime errors and ensures your networking code works reliably across different deployment environments.