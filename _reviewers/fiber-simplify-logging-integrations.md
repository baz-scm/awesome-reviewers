---
title: simplify logging integrations
description: When implementing custom logging integrations, prioritize simplicity
  and completeness over complex abstractions. Avoid creating overly complicated wrapper
  structures that developers must recreate for basic logging functionality. Instead,
  provide simple, reusable patterns that support all necessary logging levels and
  are easy to understand and maintain.
repository: gofiber/fiber
label: Logging
language: Markdown
comments_count: 2
repository_stars: 37560
---

When implementing custom logging integrations, prioritize simplicity and completeness over complex abstractions. Avoid creating overly complicated wrapper structures that developers must recreate for basic logging functionality. Instead, provide simple, reusable patterns that support all necessary logging levels and are easy to understand and maintain.

For example, when creating logger adapters, use straightforward approaches like anonymous structs with embedded functions rather than complex type definitions:

```go
func LoggerToWriter(customLogger fiberlog.AllLogger, level fiberlog.Level) io.Writer {
    return &struct {
        Write func(p []byte) (n int, err error)
    }{
        Write: func(p []byte) (n int, err error) {
            switch level {
            case fiberlog.LevelDebug:
                customLogger.Debug(string(p))
            case fiberlog.LevelInfo:
                customLogger.Info(string(p))
            case fiberlog.LevelWarn:
                customLogger.Warn(string(p))
            case fiberlog.LevelError:
                customLogger.Error(string(p))
            }
            return len(p), nil
        },
    }
}
```

Ensure that logging integrations support all relevant logging levels, not just a subset, and consider providing these patterns as reusable utilities rather than requiring each developer to implement them from scratch.