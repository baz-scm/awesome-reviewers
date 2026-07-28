---
title: Consistent, Actionable Logging
description: 'When adding/modifying logs, follow these rules:


  1) Use the Kong logging API

  - Prefer `kong.log.<level>` (e.g., `kong.log.err(...)`) over `ngx.log(...)` to keep
  logging consistent with Kong conventions.'
repository: Kong/kong
label: Logging
language: Other
comments_count: 11
repository_stars: 43871
---

When adding/modifying logs, follow these rules:

1) Use the Kong logging API
- Prefer `kong.log.<level>` (e.g., `kong.log.err(...)`) over `ngx.log(...)` to keep logging consistent with Kong conventions.

2) Pick the right level (avoid noise)
- Don’t leave payload/verbose debugging at `warn`/`err` (e.g., log payloads at `debug` only).
- Be extra cautious with logs in background workers, timers, and automated paths—debug logs can flood and be hard to disable. Log on failure, and use debug sparingly.

3) Make error messages actionable
- If the behavior is governed by a config knob, mention the knob value (e.g., “giving up after max_retry_time exceeded: X”).

4) Log enough context to diagnose failures, but in the right layer
- Include identifiers for the failing operation (entity/op/node) so support can trace what broke.
- Prefer instrumenting the function that actually performs the work (e.g., the sender/handler) rather than sprinkling one-off logs.

Example pattern:
```lua
-- Prefer kong.log over ngx.log
local ok, err = send_entries(conf, { entry })
if not ok then
  kong.log.err(string.format(
    "could not send http-log entries; giving up after max_retry_time=%d exceeded",
    conf.max_retry_time
  ))
  -- keep any success traces at debug, and avoid spamming timers
end
```

Apply this checklist across plugins, clustering/rpc, queue/timer processing, and any new debug instrumentation.