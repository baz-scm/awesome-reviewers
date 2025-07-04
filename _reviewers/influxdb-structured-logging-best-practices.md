---
title: Structured logging best practices
description: Use structured logging with appropriate field types and context to make
  logs more useful for troubleshooting. Choose specific field types over generic ones,
  include relevant metrics, and select appropriate log levels based on information
  importance.
repository: influxdata/influxdb
label: Logging
language: Go
comments_count: 5
repository_stars: 30268
---

Use structured logging with appropriate field types and context to make logs more useful for troubleshooting. Choose specific field types over generic ones, include relevant metrics, and select appropriate log levels based on information importance.

**Use appropriate field types:**
```go
// Bad: May generate excessively large logs with unpredictable content
logger.Info("TSM scheduled for compaction", zap.Any("file", group))

// Good: Clearly conveys the data with appropriate type
logger.Info("TSM scheduled for compaction", zap.Strings("files", fileNames))
```

**Include relevant context:**
```go
// Bad: Generic error with minimal context
logger.Error("error creating log writer", zap.String("path", path))

// Good: Includes specific error and context
logger.Error("error creating log writer", zap.String("path", path), zap.Error(err))
```

**Select appropriate log levels:**
```go
// Summary information at Info level
logger.Info("added files", zap.Int("count", len(fileNames)))

// Detailed information at Debug level
logger.Debug("purging", zap.Strings("files", fileNames))

// Warning for potential issues
logger.Warn("waiting for operation", zap.Duration("elapsed", elapsed))
```

For high-volume events (like dropped points), be selective about what you log to avoid overwhelming logs. Consider logging only the first N occurrences or aggregate information.