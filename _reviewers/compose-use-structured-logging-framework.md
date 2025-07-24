---
title: Use structured logging framework
description: Prefer structured logging frameworks like logrus over direct fmt output
  functions for consistency, proper log levels, and better log management. This ensures
  uniform logging behavior across the codebase and enables proper log level filtering
  and formatting.
repository: docker/compose
label: Logging
language: Go
comments_count: 2
repository_stars: 35858
---

Prefer structured logging frameworks like logrus over direct fmt output functions for consistency, proper log levels, and better log management. This ensures uniform logging behavior across the codebase and enables proper log level filtering and formatting.

Use logrus methods with appropriate log levels instead of fmt.Printf, fmt.Fprintf, or fmt.Fprintln for application messages:

```go
// Instead of:
fmt.Fprintf(s.stderr(), "Failed to parse aux message: %s", err)
_, _ = fmt.Fprintln(out, "Terminal is not a POSIX console")

// Use:
logrus.Errorf("Failed to parse aux message: %s", err)
logrus.Warning("Terminal is not a POSIX console")
```

Choose the appropriate log level (Debug, Info, Warn, Error, Fatal) based on the message severity. Reserve fmt functions only for direct user output or when specifically required to write to particular streams.