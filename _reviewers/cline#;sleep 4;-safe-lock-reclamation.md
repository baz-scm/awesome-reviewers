---
title: Safe lock reclamation
description: 'When implementing mutual-exclusion locks for concurrent script/process
  execution (e.g. filesystem-based locks via atomic `mkdir`), guard against races
  both in acquiring the lock and in reclaiming a stale one:'
repository: cline/cline#;sleep 4;
label: Concurrency
language: Shell
comments_count: 3
repository_stars: 70976
---

When implementing mutual-exclusion locks for concurrent script/process execution (e.g. filesystem-based locks via atomic `mkdir`), guard against races both in acquiring the lock and in reclaiming a stale one:

1. Acquire locks with an atomic primitive (`mkdir` fails if the directory exists), and immediately record the owner's identity — e.g. PID plus process start time — rather than relying on mtime alone, since PIDs can be reused and timestamps can be misleading.
2. Before treating a lock as abandoned, re-verify the owner is actually gone (process no longer exists or start time differs) rather than trusting a single staleness check.
3. Reclaiming a stale lock is itself a race: multiple contenders may simultaneously decide the lock is abandoned. Make reclamation atomic too — have each contender attempt to atomically claim "recovery rights" inside the specific lock instance (e.g. `mkdir lock/reclaim`), then re-check that the owner recorded in that exact instance still matches what was originally observed before destroying it. This prevents a contender that saw an old, abandoned lock from destroying a different process's legitimately-acquired successor lock.
4. Normalize any path used to construct or locate the lock (e.g. resolve `--install-dir` to an absolute path) before the lock directory is computed, so that identity checks and recovery subshells (which may `cd` into the lock dir) always address the correct location regardless of the caller's working directory.
5. Always register cleanup via `trap ... EXIT INT TERM` to release owned locks and remove partial/temporary artifacts, ensuring a killed or failing process never leaves the system in a half-finished or unrecoverable state.

Example pattern:
```bash
owner="$$ $(TZ=UTC ps -p $$ -o lstart=)"
if mkdir "$lock" 2>/dev/null; then
    printf '%s\n' "$owner" > "$lock/owner"
else
    previous=$(cat "$lock/owner" 2>/dev/null)
    # ... determine staleness by checking if $previous's PID/start-time still exists ...
    if [[ "$stale" == true ]] && mkdir "$lock/reclaim" 2>/dev/null; then
        # re-verify before destroying: has the owner changed since we observed it?
        current=$(cat "$lock/owner" 2>/dev/null)
        [[ "$current" == "$previous" ]] && rm -rf "$lock"
    fi
fi
trap 'rm -rf "$temporary"; rmdir "$lock" 2>/dev/null' EXIT INT TERM
```

Apply this double-checked, identity-based locking pattern any time concurrent processes must coordinate through shared external state (files, directories, or other non-language-level synchronization), not just in shell scripts.</description>
</invoke>
