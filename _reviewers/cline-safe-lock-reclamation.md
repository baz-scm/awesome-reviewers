---
title: Safe lock reclamation
description: 'When implementing cross-process synchronization with filesystem primitives
  (e.g. `mkdir` as a mutex), avoid time-of-check-to-time-of-use races between detecting
  a stale lock and acting on it. Treat lock recovery as its own critical section:'
repository: cline/cline
label: Concurrency
language: Shell
comments_count: 3
repository_stars: 70886
---

When implementing cross-process synchronization with filesystem primitives (e.g. `mkdir` as a mutex), avoid time-of-check-to-time-of-use races between detecting a stale lock and acting on it. Treat lock recovery as its own critical section:

1. Record enough owner identity in the lock (PID plus process start time, not just PID) so staleness checks aren't fooled by PID reuse.
2. Never reclaim a lock based on a staleness check alone — a legitimate new owner may acquire it between your check and your reclaim. Instead, enter the specific lock directory and atomically claim a nested "reclaim" marker (e.g. `mkdir lock/reclaim`) so only one contender can attempt recovery, then re-read and re-verify the owner identity *after* the claim and immediately before any destructive action.
3. Resolve all paths (install dirs, lock paths) to absolute paths before constructing lock paths or `cd`-ing into them for recovery; verify directory identity with something like `[[ "$lock" -ef . ]]` before deleting, since relative paths can silently resolve to the wrong location once the working directory changes.
4. Always register cleanup via `trap ... EXIT INT TERM` to release owned locks and remove partial/temporary artifacts, and add regression tests that simulate concurrent contenders racing to acquire/reclaim the same lock to catch these races before they ship.

Example pattern for a safe reclaim:
```bash
if [[ "$stale" == true ]]; then
    (
        cd "$lock" 2>/dev/null || exit 0
        mkdir reclaim 2>/dev/null || exit 0   # atomic claim to recover
        current=$(cat owner 2>/dev/null || true)
        # re-verify the owner is still abandoned AND we're still looking
        # at the same directory before destroying anything
        [[ "$current" == "$previous" && "$lock" -ef . ]] && rm -rf "$lock"
    )
fi
```
This pattern — atomic claim, re-verify, then act — generalizes to any manually-implemented lock/mutex and should be applied whenever recovery or cleanup logic runs concurrently with other potential lock holders.