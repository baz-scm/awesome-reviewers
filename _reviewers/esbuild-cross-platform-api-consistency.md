---
title: cross-platform API consistency
description: Design APIs to provide consistent behavior and user experience across
  different runtime environments and module systems. Abstract platform-specific differences
  behind a uniform interface so users don't need to handle environment-specific logic.
repository: evanw/esbuild
label: API
language: TypeScript
comments_count: 2
repository_stars: 39161
---

Design APIs to provide consistent behavior and user experience across different runtime environments and module systems. Abstract platform-specific differences behind a uniform interface so users don't need to handle environment-specific logic.

When designing APIs that run on multiple platforms (Node.js, Deno, browsers), ensure that:
- Core functionality works the same way regardless of the underlying platform
- Platform-specific optimizations (like `process.unref()` in Node vs Deno) are handled internally
- Export formats support both ESM and CommonJS consumption patterns
- Users can write the same code regardless of their target environment

For example, instead of requiring users to call different cleanup methods per platform:
```typescript
// Bad: Platform-specific API
if (isDeno) {
  await esbuild.stop(); // Required in Deno
} else {
  // Node handles cleanup automatically
}

// Good: Consistent API
await esbuild.stop(); // Works the same everywhere, with internal platform handling
```

This approach reduces cognitive load for API consumers and prevents environment-specific bugs in user code.