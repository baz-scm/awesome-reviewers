---
title: Use structured logging framework
description: Replace all console.* calls with an appropriate structured logging framework
  using proper log levels. This ensures consistent logging patterns, better log management,
  and appropriate handling of different severity levels.
repository: langfuse/langfuse
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 13574
---

Replace all console.* calls with an appropriate structured logging framework using proper log levels. This ensures consistent logging patterns, better log management, and appropriate handling of different severity levels.

Key guidelines:
- Use logger.debug() for development/troubleshooting information
- Use logger.info() for general operational information
- Use logger.warn() for concerning but non-critical issues
- Use logger.error() for critical issues and errors
- Pass objects directly to logger instead of string interpolation

Example:
```typescript
// Don't do this:
console.log("Processing batch:", JSON.stringify(batch));
console.warn("Redis client not available");
console.error("Failed to process:", error);

// Do this instead:
logger.info("Processing batch", { batch });
logger.warn("Redis client not available");
logger.error("Failed to process", { error });
```

This approach provides better log management, filtering capabilities, and consistent logging patterns across the codebase.