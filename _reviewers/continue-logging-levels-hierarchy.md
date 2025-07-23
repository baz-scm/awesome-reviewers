---
title: Logging levels hierarchy
description: Use appropriate logging levels to prevent debug noise from leaking into
  production environments. Reserve console.log() for important application events,
  and use console.debug() for development information that should not be visible to
  end users.
repository: continuedev/continue
label: Logging
language: TSX
comments_count: 2
repository_stars: 27819
---

Use appropriate logging levels to prevent debug noise from leaking into production environments. Reserve console.log() for important application events, and use console.debug() for development information that should not be visible to end users.

Example:
```typescript
// Avoid: Debug information using console.log
console.log("Required fields values:", required);

// Better: Use console.debug for development information
console.debug("Required fields values:", required);

// Best: Remove debug logs before production deployment or implement
// a logging framework that controls log visibility by environment
```

This practice reduces noise in production logs, making important messages more visible while still allowing developers to include helpful debugging information during development.