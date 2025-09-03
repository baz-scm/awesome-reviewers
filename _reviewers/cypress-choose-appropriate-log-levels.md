---
title: Choose appropriate log levels
description: Select log levels based on the intended audience and actionability of
  the message. Use `debug` for internal development information that helps with troubleshooting,
  `warn` or `error` for user-actionable issues, and avoid logging messages that add
  noise without providing value to the user.
repository: cypress-io/cypress
label: Logging
language: JavaScript
comments_count: 4
repository_stars: 48850
---

Select log levels based on the intended audience and actionability of the message. Use `debug` for internal development information that helps with troubleshooting, `warn` or `error` for user-actionable issues, and avoid logging messages that add noise without providing value to the user.

Key principles:
- Don't log messages users cannot act upon - this creates noise in console output
- Use `debug` logs for internal state and development information
- Ensure log formatting doesn't depend on specific log levels being enabled
- User-facing logs should provide clear, actionable information

Example:
```javascript
// Good: Internal information for developers
debug('launch project')

// Good: User-actionable warning
logger.warn(stripIndent(msg))

// Avoid: Noise that users can't act on
console.warn(`Could not get the original source file from line "${line}"`)
```

When in doubt, prefer `debug` logs for internal information and reserve user-facing logs for messages that require user attention or action.