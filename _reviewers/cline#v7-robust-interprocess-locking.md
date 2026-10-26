---
title: Robust interprocess locking
description: When you need to serialize operations across multiple processes/machines,
  implement interprocess locks with (1) verifiable ownership, (2) safe stale/abandoned
  recovery, (3) race-safe reclamation, and (4) cleanup that runs on failure.
repository: cline/cline#v7
label: Concurrency
language: Shell
comments_count: 2
repository_stars: 70865
---

When you need to serialize operations across multiple processes/machines, implement interprocess locks with (1) verifiable ownership, (2) safe stale/abandoned recovery, (3) race-safe reclamation, and (4) cleanup that runs on failure.

Practical rules:
- Use a lock “directory” (or equivalent) and store ownership metadata inside it.
- Record owner identity in a way you can verify later: e.g., **PID + UTC process start time** (not just PID or timestamps).
- Reclaim locks only when the recorded owner is confirmed dead (owner PID not running, or start time mismatches).
- Handle abandoned initialization: detect cases where a contender created the lock but the owner never finished writing valid metadata.
- During recovery/reclaim, **recheck** that you’re still reclaiming the same lock generation—never reclaim a successor lock created after you observed the stale one.
- Make lock paths stable: **normalize/absolutize any user-provided directory before constructing lock paths** so recovery processes target the same location.
- Ensure cleanup covers signals/exit: remove owned locks and temporary partial state on EXIT/INT/TERM.
- Add regression tests for: abandoned lock initialization, stale owner PID, and recovery when downloads/critical steps must not partially run.

Example (pattern):
```bash
set -euo pipefail
lock_dir="$install_dir/.install-lock"
owner_file="$lock_dir/owner"
mkdir -p "$install_dir"

# Normalize paths before using lock_dir (if derived from user input)
# install_dir="$(cd "${install_dir}" && pwd)"  # if needed

owner="$$ $(TZ=UTC ps -p $$ -o lstart=)"
cleanup() {
  # Only remove if we still own it
  if [[ -d "$lock_dir" && -f "$owner_file" ]] && grep -qx "$owner" "$owner_file"; then
    rm -rf "$lock_dir"
  fi
}
trap cleanup EXIT INT TERM

while true; do
  if mkdir "$lock_dir" 2>/dev/null; then
    printf '%s
' "$owner" > "$owner_file"
    break
  fi

  previous="$(cat "$owner_file" 2>/dev/null || true)"
  prev_pid="${previous%% *}"

  # Reclaim only if verified stale/abandoned
  stale=false
  if [[ "$prev_pid" =~ ^[0-9]+$ ]]; then
    # Confirm owner is no longer running with same start time
    [[ "$previous" == "$prev_pid $(TZ=UTC ps -p "$prev_pid" -o lstart= 2>/dev/null)" ]] || stale=true
  else
    # Missing/invalid owner metadata: treat as abandoned
    [[ -z "$previous" ]] && stale=true
  fi

  if [[ "$stale" == true ]]; then
    # Race-safe recovery: reclaim only if lock has not been replaced
    # (e.g., re-read owner_file and ensure it is still the same 'previous' value)
    current="$(cat "$owner_file" 2>/dev/null || true)"
    [[ "$current" == "$previous" ]] || continue
    rm -rf "$lock_dir"
    continue
  fi

  sleep 0.5
done

# ... critical serialized work here ...
```

Use this approach any time concurrent processes can touch shared state (downloads, installs, migrations, shared caches) to prevent race conditions, orphaned partial artifacts, and incorrect lock stealing.