---
title: Concurrency primitive semantics
description: 'When introducing async work, retries, or batching:


  1) Use each concurrency primitive for its intended role

  - Don’t repurpose a queue as a parallel executor. If you need the same per-entry
  logic from both the queue and direct callers, extract it into a shared function/module
  and have both paths call it.'
repository: Kong/kong
label: Concurrency
language: Other
comments_count: 10
repository_stars: 43871
---

When introducing async work, retries, or batching:

1) Use each concurrency primitive for its intended role
- Don’t repurpose a queue as a parallel executor. If you need the same per-entry logic from both the queue and direct callers, extract it into a shared function/module and have both paths call it.

2) Make concurrency-limit meanings unambiguous
- Define clearly what values mean “disabled” vs “unlimited” (and keep it consistent across the codebase). If you choose a sentinel (e.g. `-1`), document it where the option is read and ensure callers won’t assume `0` means unlimited.

3) Prefer mutex helpers over ad-hoc lock code
- Use shared lock helpers (e.g., `concurrency.with_worker_mutex`) to avoid race bugs and to centralize lock/timeout/exptime behavior.

4) Be careful with timers under locks
- Avoid unnecessary timers for already-asynchronous “notification” steps when the cost is negligible.
- When retrying, decide whether to release the mutex or retry while holding it, and treat lock-timeout separately from real failures.
- Don’t rely on tail-recursive timer creation; if a timer callback may be scheduled via tail recursion, schedule with a small delay instead of `0` to avoid timer stack/callsite issues.

5) Avoid timer fan-out in batch code
- If batch items would each spawn timers, consider doing the batch synchronously (or waiting for all spawned work) to prevent runaway scheduling.

Example pattern (mutex helper + safe reschedule):
```lua
local function retrying_sync(premature, retry_count)
  if premature then return end

  local res, err = concurrency.with_worker_mutex({
    name = "get_delta",
    timeout = 0,
    exptime = 5,
  }, function()
    return do_sync() -- shared logic; retry decision handled outside if needed
  end)

  if not res and err ~= "timeout" then
    ngx_log(ngx_ERR, "sync failed: ", err)
    return
  end

  -- avoid tail-recursion/timerng crash cases
  kong.timer:at(0.1, retrying_sync, (retry_count or 0) + 1)
end
```

Apply this standard during review by checking: (a) are primitives used for their intended semantics, (b) are unlimited/concurrency-limit semantics consistent, (c) are mutex/timer interactions safe under contention, and (d) does batch logic avoid uncontrolled timer spawning.