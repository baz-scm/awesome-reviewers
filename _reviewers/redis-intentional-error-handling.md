---
title: Intentional Error Handling
description: 'Handle errors based on intent: make operations idempotent for known
  conflicts, and explicitly classify/propagate errors for known transient conditions.'
repository: redis/redis
label: Error Handling
language: Other
comments_count: 2
repository_stars: 74261
---

Handle errors based on intent: make operations idempotent for known conflicts, and explicitly classify/propagate errors for known transient conditions.

Apply this standard in test scripts and helper utilities:
- For deterministic conflicts (e.g., resource already exists), use the command’s recovery flag rather than letting the call fail.
- For remote/cluster calls, wrap the call in `catch`, and:
  - Treat known transient routing issues (e.g., `MOVED*`, `ASK*`) as recoverable (retry/continue).
  - Re-raise anything else immediately so real bugs don’t get masked.

Example patterns:

```tcl
# Known conflict: make restore idempotent
catch {r restore key 0 $crafted replace} err

# Known transient cluster routing: ignore MOVED/ASK, fail fast otherwise
if {$cluster_load == 1} {
    if {[catch {$r read} err]} {
        if {[string match {MOVED*} $err] || [string match {ASK*} $err]} {
            continue
        }
        error $err
    }
} else {
    $r read
}
```