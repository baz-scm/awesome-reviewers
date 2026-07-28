---
title: Actionable logging rules
description: 'Adopt consistent logging practices:


  - **Never allow correctness-affecting failures to be silent**, especially inside
  OpenResty async callbacks (e.g., `ngx.timer.at`, log phase). Log each error path
  *inside* the callback.'
repository: apache/apisix
label: Logging
language: Other
comments_count: 11
repository_stars: 16922
---

Adopt consistent logging practices:

- **Never allow correctness-affecting failures to be silent**, especially inside OpenResty async callbacks (e.g., `ngx.timer.at`, log phase). Log each error path *inside* the callback.
- **Avoid noisy logs for expected/controlled conditions** (e.g., rate/connection limits being reached as part of normal operation). If it will spam, downgrade/remove it.
- **Use the correct log level**: errors for unexpected failures; warn for expected degradation or shutdown paths where tests/operators shouldn’t treat it as an error.
- **Include actionable context** in every message (limits/thresholds, computed values, relevant identifiers like `service_name`), and don’t log “mystery failures.”
- **Prevent duplicate logging**: if a helper already logs, don’t log again at the caller.

Example pattern (async callback):
```lua
local function log_phase_work()
    local red, err = redis.new(conf)
    if not red then
        core.log.error("failed to create redis in log phase: ", err)
        return
    end

    local ok, incoming_err = red:do_incoming(...)
    if not ok or incoming_err then
        core.log.error("failed to deduct tokens in log phase: ", incoming_err)
        return
    end

    -- release connection etc.
end

-- If you create a timer, still log inside the callback:
ngx.timer.at(0, log_phase_work)
```

Checklist for any new log line:
1) Will it help someone detect/triage a problem?
2) Could it otherwise be silently swallowed (async)?
3) Is it expected (don’t spam WARN/ERROR)?
4) Is the level appropriate (WARN vs ERROR)?
5) Does it include the key context needed to debug (ids/values)?
6) Does another function already log the same failure?