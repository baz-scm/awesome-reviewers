---
title: Robust Lock Ownership
description: When multiple processes may modify the same shared resource (e.g., installers,
  caches, generated binaries), implement locks with verifiable ownership, safe stale/abandoned
  recovery, and cleanup that only removes locks you own.
repository: cline/cline#v22
label: Concurrency
language: Shell
comments_count: 2
repository_stars: 70886
---

When multiple processes may modify the same shared resource (e.g., installers, caches, generated binaries), implement locks with verifiable ownership, safe stale/abandoned recovery, and cleanup that only removes locks you own.

Practical standard:
1) Store ownership data in the lock (not just “a file exists”): record PID + UTC process start time, e.g. `owner="$PID $(TZ=UTC ps -p $PID -o lstart=)"`.
2) Reclaim only when the recorded owner is provably gone: compare the stored (PID, start-time) to current process info; treat mismatches as stale/abandoned.
3) Prevent lock-reclaim races: after attempting recovery/claim, recheck that the lock you’re about to use is still the successor you observed (e.g., re-read ownership after creating/claiming recovery state).
4) Ensure only-owned cleanup: on EXIT/INT/TERM, remove the lock only if the ownership metadata still matches your process.
5) Make lock paths deterministic: resolve relative directories to absolute paths before constructing any lock/recovery paths.
6) Add a regression test for abandoned-lock recovery and for deterministic behavior when installation paths are relative.

Sketch (shell-style):
```bash
set -euo pipefail
lock_dir="$install_dir/.install-lock"
mkdir -p "$install_dir"
owner="$$ $(TZ=UTC ps -p $$ -o lstart=)"
lock="$lock_dir"/lock

cleanup() {
  # Only remove if we still own the lock.
  cur_owner="$(cat "$lock" 2>/dev/null || true)"
  [[ "$cur_owner" == "$owner" ]] && rm -rf "$lock_dir"
}
trap cleanup EXIT INT TERM

# Acquire
mkdir "$lock_dir" 2>/dev/null || true
if [[ ! -f "$lock" ]]; then
  # If lock exists but no/invalid owner, treat as abandoned and reclaim after grace checks.
  # (Implement PID+UTC start-time verification here.)
  printf '%s\n' "$owner" > "$lock"
fi

# Recheck ownership after any recovery/claim step.
cur_owner="$(cat "$lock")"
[[ "$cur_owner" == "$owner" ]] || fail "lost lock to another process"
```

Apply this pattern to any concurrency-sensitive scripts/services to avoid partial writes, double-installations, and unsafe takeover of a newer lock.