---
title: Low-noise, instance-safe logs
description: 'When adding or modifying logging, follow these rules:


  1) **Attribute logs to the right component/instance**

  - Avoid process-global logging hooks/state when a per-instance logger exists.'
repository: maximhq/bifrost
label: Logging
language: Go
comments_count: 6
repository_stars: 6862
---

When adding or modifying logging, follow these rules:

1) **Attribute logs to the right component/instance**
- Avoid process-global logging hooks/state when a per-instance logger exists.
- Thread the instance-bound logger into call paths so warnings are correctly attributed.

2) **Pick the right level and avoid noise**
- Use `Debug` for informational-but-non-actionable signals that can be frequent.
- For streaming or chunked flows, **gate warnings** so they emit once per logical event (e.g., only on final chunk) rather than per chunk.

3) **Never silently fall back**
- If you fall back to a default behavior due to an error (e.g., URL parse failure), emit a warning with enough context to diagnose.

4) **Use the logging API’s formatting instead of `fmt.Sprintf`**
- Prefer `logger.Warn("...: %v", err)` over `logger.Warn(fmt.Sprintf("...: %s", err))`.

5) **Don’t bloat request/context just to move logs**
- Don’t stash ad-hoc log payloads in request context solely for later retrieval.
- Use existing streaming/middleware plumbing (e.g., dedicated completer slots) to move data explicitly.

Example patterns:

```go
// 1+3) Instance-safe warning on fallback
if err != nil {
    logger.Warn("oauth: url parse failed, falling back to direct client: %v", err)
}

// 2) Correct level + log once (stream-aware)
if isStream && !isFinalChunk {
    // skip warning
} else {
    logger.Debug("cache: skipping write (namespace=%s, id=%s): no embedding available", ns, id)
}

// 4) Prefer format args
logger.Warn("logstore: skipping index maintenance: could not acquire index lock: %v", err)

// 5) Avoid reading logs back from fasthttp context; use dedicated slot/completer
// e.g., middleware publishes into a known slot, handler drains it after stream completes.
```

Applying this consistently reduces production log spam, preserves accurate attribution, improves diagnostics when fallbacks occur, and keeps logging implementation clean and maintainable.