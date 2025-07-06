---
title: Contextual structured logging
description: Log messages should provide sufficient context to be meaningful and actionable
  while following structured logging patterns. Include relevant metrics, ratios, or
  identifiers that help diagnose issues. Use semantic conventions and structured key-value
  pairs rather than embedding values in message strings.
repository: grafana/grafana
label: Logging
language: Go
comments_count: 2
repository_stars: 68825
---

Log messages should provide sufficient context to be meaningful and actionable while following structured logging patterns. Include relevant metrics, ratios, or identifiers that help diagnose issues. Use semantic conventions and structured key-value pairs rather than embedding values in message strings.

Example (Before):
```go
logger.Info("empty refid found", "query_count", len(queries))
```

Example (After):
```go
logger.Info("empty refid found", "empty_count", 1, "query_count", len(queries))
```

For error logging, use structured logging with semantic conventions:
```go
// Prefer this
log.ErrorReason(gfErr.Reason)

// Over this
log.Info("errorReason", gfErr.Reason, "error", gfErr.LogMessage)
```

Well-structured logs with proper context improve observability and make debugging more efficient across the entire system.