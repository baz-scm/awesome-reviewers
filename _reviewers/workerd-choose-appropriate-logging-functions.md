---
title: Choose appropriate logging functions
description: Select the correct logging function based on frequency, severity, and
  destination to avoid log spam and ensure proper routing. Use LOG_ONCE or LOG_PERIODICALLY
  for repeated warnings that could spam logs, KJ_LOG(ERROR) for general error logging,
  and LOG_EXCEPTION only for exceptions intended for Sentry monitoring.
repository: cloudflare/workerd
label: Logging
language: Other
comments_count: 2
repository_stars: 6989
---

Select the correct logging function based on frequency, severity, and destination to avoid log spam and ensure proper routing. Use LOG_ONCE or LOG_PERIODICALLY for repeated warnings that could spam logs, KJ_LOG(ERROR) for general error logging, and LOG_EXCEPTION only for exceptions intended for Sentry monitoring.

For repeated warnings that could spam logs:
```cpp
// Instead of:
KJ_LOG(WARNING, "jurisdiction restrictions have no affect in workerd", jurisdiction);

// Use:
KJ_LOG_ONCE(WARNING, "jurisdiction restrictions have no affect in workerd", jurisdiction);
// or
KJ_LOG_PERIODICALLY(WARNING, "jurisdiction restrictions have no affect in workerd", jurisdiction);
```

For exception logging, choose based on destination:
```cpp
// For general error logging:
KJ_LOG(ERROR, "test failed with exception", exception);

// Only for Sentry-bound exceptions:
LOG_EXCEPTION("test", exception);
```

This prevents log flooding, ensures appropriate log routing, and maintains clean, actionable log output across different environments.