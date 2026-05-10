---
title: Logging Correctness Rules
description: 'When adding or modifying logging:


  1) **Match logging intent to behavior (level + visibility)**

  - If a user-supplied config or runtime option fails and a fallback happens, log
  at an appropriate user-visible level (often `warning`)—don’t silently continue.'
repository: celery/celery
label: Logging
language: Python
comments_count: 7
repository_stars: 28464
---

When adding or modifying logging:

1) **Match logging intent to behavior (level + visibility)**
- If a user-supplied config or runtime option fails and a fallback happens, log at an appropriate user-visible level (often `warning`)—don’t silently continue.
- For shutdown/termination paths that users expect to see (effectively “exit”), emit a **critical** log and then exit/raise a clean termination exception.

2) **Avoid brittle or expensive caller-location tricks**
- Don’t rely on fragile `stacklevel` or heavy `inspect.stack()` to make warnings point to the “right” caller—especially when call paths can be indirect.
- Prefer: emit the warning with a reasonable stacklevel or remove the warning if it’s not truly actionable.

3) **Keep log output formatting deterministic**
- Ensure logging proxies/stream redirects handle newlines/buffering so traceback/console output isn’t fragmented.
- Be careful with whitespace transforms (`strip()`, removing newlines) because it can change observed output and backward compatibility.

4) **Use the right channel depending on logging configuration availability**
- Prefer the logging module when it’s configured.
- If logs may not be configured yet (early startup/deployment messaging), using `sys.stderr` is acceptable—goal is visibility, not configuration purity.

Example (recommended patterns):

```python
import sys
import logging
logger = logging.getLogger(__name__)

# 1) User-visible fallback
try:
    task_id = str(task_id_generator())
except Exception as exc:
    logger.warning(
        "Custom task_id_generator failed, falling back to UUID: %s: %s",
        type(exc).__name__, exc,
    )

# 2) Fatal path: critical log + clean shutdown
logger.critical("Retrying to establish connection after connection loss is disabled; shutting down")
raise SystemExit(1)

# 4) Early/deployment message when logging may be unavailable
print("Broken pidfile found", file=sys.stderr)

# 3) Line-buffered proxy write (avoid fragmented output)
class LoggingProxy:
    def __init__(self, logger, loglevel=logging.INFO):
        self.logger = logger
        self.loglevel = loglevel
        self._buffer = ""
        self.closed = False

    def write(self, data: str):
        if not data or self.closed:
            return 0
        self._buffer += str(data)
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line:
                self.logger.log(self.loglevel, line)
        return len(data)
```

Adopting these rules prevents misleading or noisy logs, keeps console/traceback output intact, and avoids performance/accuracy pitfalls in warning/caller handling.