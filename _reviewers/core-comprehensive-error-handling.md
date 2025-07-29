---
title: comprehensive error handling
description: Ensure error handling mechanisms are comprehensive and graceful rather
  than limited or forceful. Use persistent event listeners (`process.on()`) instead
  of one-time listeners (`process.once()`) for critical error scenarios to handle
  all occurrences, not just the first one. Similarly, prefer graceful shutdown methods
  that allow proper cleanup over forceful...
repository: adonisjs/core
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 18071
---

Ensure error handling mechanisms are comprehensive and graceful rather than limited or forceful. Use persistent event listeners (`process.on()`) instead of one-time listeners (`process.once()`) for critical error scenarios to handle all occurrences, not just the first one. Similarly, prefer graceful shutdown methods that allow proper cleanup over forceful process termination.

For signal and exception handling:
```typescript
// Preferred: Handles all occurrences
process.on('SIGINT', this.kill)
process.on('SIGTERM', this.kill)
process.on('uncaughtException', (error) => {
  // Handle error
})

// Avoid: Only handles first occurrence
process.once('SIGINT', this.kill)
```

For application shutdown:
```typescript
// Preferred: Graceful shutdown with cleanup
await this.application.shutdown()

// Avoid: Forceful termination
await this.exit()
```

This approach ensures that all error scenarios are properly handled and allows applications to clean up resources gracefully, preventing issues like interrupted stdout or incomplete cleanup operations.