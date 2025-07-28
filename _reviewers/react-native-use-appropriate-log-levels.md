---
title: Use appropriate log levels
description: Choose logging levels that match the intended audience and purpose of
  the message. Use debug or silent logging for internal operations, optional behaviors,
  and retry logic that shouldn't be visible to end users. Reserve console output and
  higher log levels (info, warning, error) for user-relevant information.
repository: facebook/react-native
label: Logging
language: JavaScript
comments_count: 2
repository_stars: 123178
---

Choose logging levels that match the intended audience and purpose of the message. Use debug or silent logging for internal operations, optional behaviors, and retry logic that shouldn't be visible to end users. Reserve console output and higher log levels (info, warning, error) for user-relevant information.

Internal operations like workspace detection, file system probing, and retry mechanisms should use debug logging to avoid cluttering user output during normal operation. This is especially important for optional behaviors that may fail gracefully.

Example of appropriate level selection:
```javascript
// For internal/optional operations - use debug logging
try {
  const workspaceConfig = detectWorkspace(packagePath);
} catch (err) {
  if (err.code !== 'ENOENT') {
    logger.debug(`Failed getting workspace root from ${packagePath}:`, err);
  }
}

// For user-facing messages - use appropriate console levels
function prebuildLog(
  message /*: string */,
  level /*: 'info' | 'warning' | 'error' */ = 'warning',
) {
  const prefix = '[Prebuild] ';
  let colorFn = (x /*:string*/) => x;
  if (process.stdout.isTTY) {
    if (level === 'info') colorFn = x => `\x1b[32m${x}\x1b[0m`;
    else if (level === 'error') colorFn = x => `\x1b[31m${x}\x1b[0m`;
    else colorFn = x => `\x1b[33m${x}\x1b[0m`;
  }
  console.log(colorFn(prefix + message));
}
```

This approach prevents information overload while maintaining useful debugging capabilities for developers.