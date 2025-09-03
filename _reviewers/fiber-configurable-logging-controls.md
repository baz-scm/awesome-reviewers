---
title: Configurable logging controls
description: Make logging behavior configurable rather than hardcoded, and avoid manipulating
  global state for logging purposes. Provide configuration options to enable/disable
  specific log messages, especially for warnings or debug information that could become
  spammy. Instead of overwriting global variables like os.Stdout and os.Stderr for
  testing, use dependency...
repository: gofiber/fiber
label: Logging
language: Go
comments_count: 2
repository_stars: 37560
---

Make logging behavior configurable rather than hardcoded, and avoid manipulating global state for logging purposes. Provide configuration options to enable/disable specific log messages, especially for warnings or debug information that could become spammy. Instead of overwriting global variables like os.Stdout and os.Stderr for testing, use dependency injection or proper logging interfaces that can be mocked or redirected.

Example of configurable logging:
```go
type Config struct {
    EnableWarnings bool
    Logger         Logger // injectable logger interface
}

func FromContext(c fiber.Ctx) *Middleware {
    m, ok := c.Locals(middlewareContextKey).(*Middleware)
    if !ok && cfg.EnableWarnings {
        cfg.Logger.Warn("session: Session middleware not registered")
        return nil
    }
    return m
}
```

This approach prevents misleading or excessive log output while maintaining flexibility for different deployment environments and testing scenarios.