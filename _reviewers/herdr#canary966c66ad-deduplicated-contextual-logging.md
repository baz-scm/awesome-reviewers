---
title: Deduplicated, contextual logging
description: Each significant event should be logged exactly once, at the appropriate
  level, with enough structured context (e.g. a reason code, counts, or a relevant
  path) to diagnose the issue without reproducing it. Avoid routing the same logical
  event through multiple log call sites, which can produce duplicate or conflicting
  lines; instead, log it where it is most...
repository: ogulcancelik/herdr#canary966c66ad
label: Logging
language: Rust
comments_count: 4
repository_stars: 46332
---

Each significant event should be logged exactly once, at the appropriate level, with enough structured context (e.g. a reason code, counts, or a relevant path) to diagnose the issue without reproducing it. Avoid routing the same logical event through multiple log call sites, which can produce duplicate or conflicting lines; instead, log it where it is most meaningful (e.g. a shutdown reason logged once at the point the shutdown actually happens, not again in a generic shutdown handler).

For transient or repeated conditions (retries, intermittent errors), do not emit the same message on every occurrence — that only adds noise without new information. Instead, log once when the condition starts (e.g. `error!` on first failure) and once when it resolves (e.g. `info!` with a count on recovery), as in:

```rust
if consecutive_errors == 0 {
    error!(err = %err, "api listener accept failed; retrying");
}
// ... on success after failures:
if consecutive_errors > 0 {
    info!(consecutive_errors, "api listener accept recovered");
}
```

Also make sure operations that can partially succeed or fail silently (e.g. an injected input event count lower than requested) emit a `warn!`/`error!` with the actual vs. expected values, so failures leave a diagnostic trail instead of appearing as a silent success.

When adding contextual fields such as file paths, be deliberate: include them when they materially help diagnose an issue, but remember such values must be redacted before logs are shared outside the team.</description>
