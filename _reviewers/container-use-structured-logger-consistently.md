---
title: Use structured logger consistently
description: 'Adopt a single logging approach across commands and services:


  - **Never use `print`/direct `FileHandle.standardError.write` in production code**
  for user-facing or diagnostic messages. Use `Logger`.'
repository: apple/container
label: Logging
language: Swift
comments_count: 10
repository_stars: 48787
---

Adopt a single logging approach across commands and services:

- **Never use `print`/direct `FileHandle.standardError.write` in production code** for user-facing or diagnostic messages. Use `Logger`.
- **Plumb and reuse the existing logger**:
  - In `AsyncLoggableCommand`, use the provided `log`—don’t create a redundant logger.
  - In utilities/helpers, accept a `log: Logger` (or `log: Logger?` when optional) from the caller; don’t do unconditional stderr output inside the helper.
- **Use structured logging**: prefer `metadata` dictionaries over interpolating values into the message.
  - Example pattern:
    ```swift
    log.warning(
      "failed to load container",
      metadata: ["path": dir.path, "error": String(describing: error)]
    )
    ```
- **Choose appropriate levels for stderr/normal flows**: avoid logging non-error conditions to stderr; reserve `warning/error` for actionable issues, and use `debug/trace` for noisy entry/exit or busy calls.
- **Keep test diagnostics real**: when cleanup fails, log enough details to diagnose (name, error, stdout/stderr/status) rather than retrying in a way that hides the root cause.

Applying this consistently will keep stderr output clean, make logs machine-parseable, and ensure logging behavior follows configured verbosity (e.g., `--debug` should increase log level via the logger/handler, not by adding new ad-hoc prints).