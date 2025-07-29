---
title: provide contextual error information
description: Ensure error messages and logging provide sufficient context to understand
  what failed and why. Include relevant details such as server addresses, operation
  types, configuration values, or other identifying information that helps with debugging
  and troubleshooting.
repository: traefik/traefik
label: Error Handling
language: Go
comments_count: 2
repository_stars: 55772
---

Ensure error messages and logging provide sufficient context to understand what failed and why. Include relevant details such as server addresses, operation types, configuration values, or other identifying information that helps with debugging and troubleshooting.

When handling errors, especially in network operations, health checks, or resource management:

1. **Include identifying information** in error messages (server addresses, service names, etc.)
2. **Specify which operation failed** (connection, payload write, response read, etc.)
3. **Log errors with appropriate context** using structured logging
4. **Handle resource cleanup errors** explicitly rather than ignoring them

Example from health check implementation:
```go
// Instead of generic error handling
if err := thc.executeHealthCheck(ctx, thc.config, target); err != nil {
    log.Warn().Err(err).Msg("Health check failed.")
}

// Provide specific context about what failed
if err := thc.executeHealthCheck(ctx, thc.config, target); err != nil {
    log.Ctx(ctx).Warn().
        Str("targetURL", target.String()).
        Str("service", thc.serviceName).
        Err(err).
        Msg("Health check failed.")
}

// Handle resource cleanup with error context
defer func() {
    if err := conn.Close(); err != nil {
        log.Ctx(ctx).Warn().
            Err(err).
            Str("target", target.String()).
            Msg("Failed to close health check connection")
    }
}()
```

This approach significantly improves debugging capabilities and system observability by making it clear which specific component, server, or operation encountered the error.