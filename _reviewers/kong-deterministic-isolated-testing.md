---
title: Deterministic isolated testing
description: 'Make integration/unit tests deterministic, isolated, and robust against
  async timing and ordering.


  Checklist

  - **No ordering dependence:** Each test must be runnable alone; avoid modifying
  a shared plugin/config mid-suite. For configuration permutations, create separate
  routes/services (or fully separate instances) per permutation.'
repository: Kong/kong
label: Testing
language: Other
comments_count: 9
repository_stars: 43871
---

Make integration/unit tests deterministic, isolated, and robust against async timing and ordering.

Checklist
- **No ordering dependence:** Each test must be runnable alone; avoid modifying a shared plugin/config mid-suite. For configuration permutations, create separate routes/services (or fully separate instances) per permutation.
- **Explicit state transitions:** If testing readiness/convergence, assert the initial “not ready” state first (e.g., 503) and then assert the “ready” state.
- **Single timeout strategy:** If you use a helper like `pwait_until/assert.eventually`, don’t add extra per-assert timeouts unless you truly need nested waits.
- **Synchronize to server-side truth:** Don’t rely on client-side sleeps or random timing for timing-sensitive behavior. Prefer waiting on server time/state/metrics/log lines until the expected condition is satisfied.
- **Right bounds to reduce flakiness:** Keep iteration counts/time windows just large enough; higher counts increase the chance of crossing period boundaries.
- **Guaranteed cleanup:** Ensure `teardown()`/cleanup stops every started component and closes clients even if earlier assertions fail.

Example pattern (Lua)
```lua
describe("readiness", function()
  lazy_setup(function()
    assert(start_kong_dp())
  end)

  lazy_teardown(function()
    -- always stop what we started
    assert(helpers.stop_kong("serve_dp"))
  end)

  it("transitions to ready", function()
    local res = helpers.http_client("127.0.0.1", tcp_status_port):get("/status/ready")
    assert.res_status(503, res) -- assert initial state

    assert.with_timeout(30).eventually(function()
      local r = helpers.http_client("127.0.0.1", tcp_status_port):get("/status/ready")
      assert.res_status(200, r)
    end)
  end)
end)
```

Apply this standard whenever tests touch CP/DP sync, rate limiting/period counters, metrics/log convergence, or any configuration that can be mutated across tests.