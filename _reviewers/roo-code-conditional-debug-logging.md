---
title: Conditional debug logging
description: Remove or conditionally disable console.log and console.debug statements
  before committing code to production. These debugging statements create noise in
  browser consoles, may expose sensitive information, and can impact runtime performance.
repository: RooCodeInc/Roo-Code
label: Logging
language: TSX
comments_count: 4
repository_stars: 17288
---

Remove or conditionally disable console.log and console.debug statements before committing code to production. These debugging statements create noise in browser consoles, may expose sensitive information, and can impact runtime performance.

Instead of using direct console logging statements, implement a logging utility that respects environment settings:

```typescript
// logger.ts
export const logger = {
  debug: (message: string, ...args: any[]) => {
    if (process.env.NODE_ENV === 'development' || localStorage.getItem('debug-enabled') === 'true') {
      console.debug(`[DEBUG] ${message}`, ...args);
    }
  },
  log: (message: string, ...args: any[]) => {
    if (process.env.NODE_ENV === 'development' || localStorage.getItem('debug-enabled') === 'true') {
      console.log(`[LOG] ${message}`, ...args);
    }
  },
  // Always show warnings and errors
  warn: (message: string, ...args: any[]) => console.warn(`[WARN] ${message}`, ...args),
  error: (message: string, ...args: any[]) => console.error(`[ERROR] ${message}`, ...args),
};

// Usage example - replaces instances like:
// console.log(`McpErrorRow level: ${error.level} for message: ${error.message.substring(0, 20)}...`)
// With:
logger.debug(`McpErrorRow level: ${error.level} for message: ${error.message.substring(0, 20)}...`);
```

For test files, remove all debugging statements entirely to keep test output clean. Consider adding a linting rule to catch accidental console statements before they reach code review.