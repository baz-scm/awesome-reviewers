---
title: Add contextual logging
description: Add informative log messages with sufficient context to help operators
  diagnose issues, understand system state, and trace complex operations. Include
  relevant error details, system configuration status, and operational flow information.
repository: gravitational/teleport
label: Logging
language: Go
comments_count: 4
repository_stars: 19109
---

Add informative log messages with sufficient context to help operators diagnose issues, understand system state, and trace complex operations. Include relevant error details, system configuration status, and operational flow information.

Key practices:
- Log system initialization status with context about why components succeeded or failed
- Include error details when operations fail to help with troubleshooting
- Add debug logs for complex flows like handshakes, authentication, and multi-step operations
- Ensure error logging is consistent across different code paths and roles
- Provide actionable information in log messages for administrators

Example from user accounting initialization:
```go
utmp, utmpErr := NewUtmpBackend(cfg.UtmpFile, cfg.WtmpFile, cfg.BtmpFile)
if utmpErr == nil {
    uacc.utmp = utmp
    slog.DebugContext(ctx, "utmp user accounting is active")
}
wtmpdb, wtmpdbErr := NewWtmpdbBackend(cfg.WtmpdbFile)
if wtmpdbErr == nil {
    uacc.wtmpdb = wtmpdb
    slog.DebugContext(ctx, "wtmpdb user accounting is active")
}
if uacc.utmp == nil && uacc.wtmpdb == nil {
    slog.DebugContext(
        ctx, "no user accounting backends are available, sessions will not be logged locally",
        "utmp_error", utmpErr, "wtmpdb_error", wtmpdbErr,
    )
}
```

This approach helps operators understand what's happening in the system and provides the context needed to resolve issues when they occur.