---
title: Remove production console logs
description: Console logs should not appear in production code, especially debug statements
  that can expose sensitive information or clutter output. When error logging is necessary,
  log detailed information internally while presenting sanitized messages to users.
repository: cline/cline
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 48299
---

Console logs should not appear in production code, especially debug statements that can expose sensitive information or clutter output. When error logging is necessary, log detailed information internally while presenting sanitized messages to users.

Remove debug console.log statements before merging to production. For legitimate error handling, use proper error logging that separates internal details from user-facing messages.

Example of proper error logging:
```typescript
} catch (err) {
    // Log full error details internally for debugging
    console.error(`Error during Claude Code execution:`, err)
    
    // Show sanitized message to user
    throw new Error(`Claude Code process failed.${errorOutput ? ` Error: ${errorOutput}` : ""}`)
}
```

Be particularly strict with files that handle sensitive data or user interactions. Consider adding code comments or linting rules to prevent console logs from being reintroduced in critical files.