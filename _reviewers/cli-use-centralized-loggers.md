---
title: Use centralized loggers
description: Always use centrally supplied loggers from the invocation context or
  configuration instead of creating new logger instances, using log.Default(), or
  direct output methods like fmt.Println(). This ensures consistent debug configuration,
  proper log level control, and centralized logging behavior across the entire application.
repository: snyk/cli
label: Logging
language: Go
comments_count: 8
repository_stars: 5178
---

Always use centrally supplied loggers from the invocation context or configuration instead of creating new logger instances, using log.Default(), or direct output methods like fmt.Println(). This ensures consistent debug configuration, proper log level control, and centralized logging behavior across the entire application.

Creating new loggers bypasses the centralized configuration and can result in logs appearing even when debugging is disabled, or missing important configuration like log levels and output destinations.

**Preferred approach:**
```go
// Use logger from invocation context
debugLogger := invocation.GetEnhancedLogger()
debugLogger.Printf("Command timeout set for %d seconds", timeout)

// Or use centrally configured logger with wrapper when needed
p.DebugLogger = log.New(&gafUtils.ToZeroLogDebug{Logger: debugLogger}, "", 0)
```

**Avoid:**
```go
// Don't create new loggers
zerologLogger := zerolog.New(os.Stderr).With().Timestamp().Logger()

// Don't use defaults that bypass central configuration  
p.authenticator = httpauth.NewProxyAuthenticator(p.authMechanism, p.upstreamProxy, log.Default())

// Don't use direct output methods
fmt.Println("Error deleting an old version directory")
```

This practice ensures that all logging respects the debug configuration and logger settings that are centrally managed, providing consistent behavior and proper control over log output.