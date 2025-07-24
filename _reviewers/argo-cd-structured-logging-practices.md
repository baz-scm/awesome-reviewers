---
title: structured logging practices
description: Use structured logging with proper context and consolidate related log
  messages. Instead of multiple separate log statements or string interpolation, use
  structured fields that are parseable by log tools and provide sufficient context
  for debugging.
repository: argoproj/argo-cd
label: Logging
language: Go
comments_count: 5
repository_stars: 20149
---

Use structured logging with proper context and consolidate related log messages. Instead of multiple separate log statements or string interpolation, use structured fields that are parseable by log tools and provide sufficient context for debugging.

Key practices:
1. **Use structured fields**: Log data as separate fields rather than interpolating into messages
2. **Consolidate related messages**: Combine multiple related log statements into a single structured message
3. **Provide adequate context**: Include relevant identifiers (like revision, repo URL, application name) as structured fields
4. **Use standard field names**: Follow established conventions (e.g., "application" instead of "app")
5. **Initialize fields properly**: Start with empty structured field sets and populate as needed

Example:
```go
// Instead of:
log.Warnf("Failed to verify token: %s", err)
log.Infof("Client IP: %s", r.RemoteAddr)

// Use:
log.WithFields(log.Fields{
    "client_ip": r.RemoteAddr,
    "error": err,
}).Warn("Failed to verify token")

// For application logs, use standard fields:
logCtx.WithField("application", appName).Errorf("validation error: %s", message)
```

This approach makes logs more searchable, reduces noise, and provides better context for troubleshooting.