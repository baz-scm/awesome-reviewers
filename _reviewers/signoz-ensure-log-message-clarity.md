---
title: Ensure log message clarity
description: Log messages should be clear, unambiguous, and avoid creating confusion
  for developers and operators. This means explicitly logging when no-op operations
  occur (rather than staying silent) and avoiding duplicate log entries with identical
  information that can mislead readers.
repository: SigNoz/signoz
label: Logging
language: Go
comments_count: 2
repository_stars: 23369
---

Log messages should be clear, unambiguous, and avoid creating confusion for developers and operators. This means explicitly logging when no-op operations occur (rather than staying silent) and avoiding duplicate log entries with identical information that can mislead readers.

Silent operations in dependency injection scenarios can be particularly dangerous as they hide important system behavior. Always add explicit logging to indicate when no-op implementations are being called.

Similarly, avoid logging the same information multiple times with identical fields, as this creates confusion about whether multiple events occurred or if there's a logging bug.

Example of good practice:
```go
func (provider *provider) Send(ctx context.Context, messages ...analyticstypes.Message) {
    // Explicitly log the no-op behavior
    provider.logger.Debug("noop analytics provider called - no messages will be sent")
}

// Instead of logging both error and info with same fields:
if err != nil {
    fields = append(fields, zap.Error(err))
    middleware.logger.Error(logMessage, fields...)
    return // Don't also log info
}
middleware.logger.Info(logMessage, fields...)
```