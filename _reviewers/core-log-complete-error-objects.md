---
title: log complete error objects
description: Always log complete error objects rather than just error messages to
  preserve stack traces, error codes, and debugging context. Use the application's
  logger instead of hardcoded console statements in modules.
repository: adonisjs/core
label: Logging
language: TypeScript
comments_count: 4
repository_stars: 18071
---

Always log complete error objects rather than just error messages to preserve stack traces, error codes, and debugging context. Use the application's logger instead of hardcoded console statements in modules.

When catching errors, log the entire error object to capture all available debugging information:

```ts
// ❌ Avoid - loses valuable debugging context
catch (error) {
  this.logger.error(`unable to install dependencies: ${error.message}`)
}

// ✅ Preferred - preserves complete error information
catch (error) {
  this.logger.fatal(error)
  // or with additional context
  this.logger.error('Unable to install dependencies', error)
}
```

Modern loggers can handle error objects properly without manual formatting like JSON.stringify(). Reserve console methods only for user-facing messages that must remain separate from structured application logs.