---
title: Use centralized logging framework
description: Always use the established logging infrastructure instead of creating
  custom logging solutions or multiple logging systems. This prevents fragmentation
  and ensures consistent log management across the codebase.
repository: menloresearch/jan
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 37620
---

Always use the established logging infrastructure instead of creating custom logging solutions or multiple logging systems. This prevents fragmentation and ensures consistent log management across the codebase.

When you need logging functionality, leverage the existing logging framework (like `@janhq/core/node` log function) rather than implementing ad-hoc solutions. If additional features like log levels are needed, extend the central framework rather than creating parallel systems.

Avoid patterns like:
```typescript
// Don't create custom debug wrappers
export const debugInspectorSync = process.env.DEBUG ? debugInspector(setBinPath) : setBinPath

// Don't implement separate file logging
subprocess.stderr.on("data", (data) => {
  fs.writeFileSync("nitro-err.txt", data); // Avoid this
});
```

Instead, use the centralized approach:
```typescript
import { log } from "@janhq/core/node";

// Use the established logging system
log("Debug info", data);
```

This approach ensures all logging goes through a unified system that can handle log routing, formatting, and management consistently.