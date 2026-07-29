---
title: Bounded Hot-Path Work
description: In performance-sensitive hot paths, ensure you (1) don’t repeat expensive
  work, (2) keep async/event-loop paths non-blocking, (3) bound external operations
  with finite timeouts, and (4) avoid unnecessary computation/materialization by prefiltering
  queries and projecting only what’s needed.
repository: nousresearch/hermes-agent
label: Performance Optimization
language: Python
comments_count: 9
repository_stars: 221948
---

In performance-sensitive hot paths, ensure you (1) don’t repeat expensive work, (2) keep async/event-loop paths non-blocking, (3) bound external operations with finite timeouts, and (4) avoid unnecessary computation/materialization by prefiltering queries and projecting only what’s needed.

Practical rules:
- Probe once, reuse everywhere: if you need media metadata (e.g., audio duration), compute it once per request and pass the result to both upload and downstream message payloads.
- Never run hung external tools without timeouts: wrap subprocess calls (ffprobe, git fetch, etc.) with explicit timeouts and test the timeout path.
- Make conditional SQL/JOINs match output mode: when a “compact” flag is set, don’t select/join/materalize columns you won’t use.
- Eliminate N+1 database scans: prefilter candidates in SQL before loading related rows (e.g., avoid loading all tasks then fetching comments per task).
- Enforce budgets strictly at append/truncation time: check remaining capacity and truncate/reject the next section before adding it, then assert final aggregate size.
- Verify timer/cadence logic with edge cases: clamping must be strictly ordered (e.g., fast-reconnect cutoff must be < stale timeout for all finite stale values) and cadence guards must actually satisfy the stated cadence contract.
- Use hot-path config loaders: in per-turn loops, prefer read-only/minimal-overhead loaders over deepcopy-heavy ones.

Example pattern (reused probe + bounded subprocess):
```python
async def send_audio(path, upload_fn, send_msg_fn, ffprobe_fn):
    # Probe once (prefer an async-friendly ffprobe wrapper if available)
    duration_ms = await ffprobe_fn(path, timeout=10.0)  # must be bounded

    # Upload using the same duration metadata
    media_id = await upload_fn(path, metadata={"duration_ms": duration_ms})

    # Reuse for message payload (no second probe)
    return await send_msg_fn(media_id, metadata={"duration_ms": duration_ms})
```

Checklist to apply during review:
- Does this hot path compute the same expensive thing twice?
- Are subprocess/network/command invocations bounded with finite timeouts?
- Are DB queries prefiltered (no board-wide loads + per-candidate follow-ups)?
- Do query projections/joins change when “compact” or “mode flags” change?
- Are budgets/timers/cadence enforced with strict, testable ordering?
- Are per-turn/per-request utilities using the cheapest available code paths (e.g., read-only config loaders)?