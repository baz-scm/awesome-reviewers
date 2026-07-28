---
title: Avoid Duplication, Extract Helpers
description: Keep code readable and maintainable by (1) extracting complex or phase-specific
  logic into dedicated helper functions, (2) removing duplicated logic/schema/label
  definitions in favor of shared helpers or a single source of truth, and (3) following
  existing project idioms/utilities to stay consistent.
repository: apache/apisix
label: Code Style
language: Other
comments_count: 12
repository_stars: 16922
---

Keep code readable and maintainable by (1) extracting complex or phase-specific logic into dedicated helper functions, (2) removing duplicated logic/schema/label definitions in favor of shared helpers or a single source of truth, and (3) following existing project idioms/utilities to stay consistent.

How to apply:
- Extract when a function becomes long, heavily nested, or mixes concerns (e.g., operational logic vs logging/secondary phases). Create helpers like `log_phase_incoming(...)` and call them from the main path.
- Prevent drift-prone duplication: define label lists/schemas/paths once and reuse the same structure for both registration and value handling.
- Follow established conventions: use the existing utility functions for string operations (e.g., `core.string.find`), prefer the project’s standard concatenation/operator style (`..`), and use consistent response/header utilities (`core.response.set_header`).
- Scope refactors: do small, high-impact extractions/dedupes together, but avoid unrelated large structural changes in the same PR.

Example (helper extraction + phase separation):
```lua
local function log_phase_incoming_thread(premature, self, key, cost)
    local conf = self.conf
    local red, err = redis.new(conf)
    if not red then
        return red, err
    end
    return util.redis_log_phase_incoming(self, red, key, cost)
end

local function log_phase_incoming(self, key, cost, dry_run)
    if dry_run then
        return true
    end
    local ok, err = ngx_timer_at(0, log_phase_incoming_thread, self, key, cost)
    if not ok then
        core.log.error("failed to create timer: ", err)
        return nil, err
    end
    return ok
end

function _M.incoming(self, key, cost, dry_run)
    if get_phase() == "log" then
        return log_phase_incoming(self, key, cost, dry_run)
    end
    -- main phase logic...
end
```