---
title: Log effectively for debugging
description: 'Always include meaningful log messages at appropriate levels to aid
  in debugging and system monitoring. Follow these guidelines:


  1. **Never silently swallow errors** - Even during cleanup operations, log errors
  that might be helpful for debugging:'
repository: opentofu/opentofu
label: Logging
language: Go
comments_count: 8
repository_stars: 25901
---

Always include meaningful log messages at appropriate levels to aid in debugging and system monitoring. Follow these guidelines:

1. **Never silently swallow errors** - Even during cleanup operations, log errors that might be helpful for debugging:
   ```go
   // Bad: Silently ignoring errors
   os.Chdir(oldDir)
   
   // Good: Log errors even if they're not fatal
   if err := os.Chdir(oldDir); err != nil {
       log.Printf("[WARN] cleanup error during directory change: %v", err)
   }
   ```

2. **Use appropriate log levels** based on severity:
   - `[TRACE]` - For detailed debugging information
   - `[DEBUG]` - For information useful during development
   - `[INFO]` - For normal operations that completed successfully
   - `[WARN]` - For recoverable problems or retryable operations
   - `[ERROR]` - For failures that impact functionality

   ```go
   // Bad: Using INFO for a failure condition
   logger.Printf("[INFO] failed to fetch provider package; retrying")
   
   // Good: Using WARN for a retryable failure
   logger.Printf("[WARN] failed to fetch provider package; retrying attempt %d/%d", i, maxHTTPPackageRetryCount)
   ```

3. **Include sufficient context** in log messages to make them actionable:
   - Identify the component/function in the message
   - Include relevant variables and state information
   - For complex operations, log inputs and outputs

   ```go
   // Bad: Generic log message
   log.Printf("[ERROR] no module call found")
   
   // Good: Contextual log message
   log.Printf("[ERROR] %s: no module call found in %q for %q", funcName, parent.Path, calledModuleName)
   ```

4. **Add trace logs for complex operations** that might need debugging in the future:
   ```go
   // In functions with complex parsing or processing
   log.Printf("[TRACE] extractImportPath input: %q", fullName)
   ```

Always consider how logs will be used by developers, operators, and users when troubleshooting issues in production environments.