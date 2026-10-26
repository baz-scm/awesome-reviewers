---
title: Safe lock ownership
description: When multiple processes may perform the same critical operation concurrently,
  enforce mutual exclusion with a lock that (1) records who owns it, (2) can safely
  recover from stale/abandoned locks, (3) only reclaims/cleans up when ownership is
  verified, and (4) prevents partial/inconsistent state.
repository: cline/cline#v9
label: Concurrency
language: Shell
comments_count: 2
repository_stars: 70868
---

When multiple processes may perform the same critical operation concurrently, enforce mutual exclusion with a lock that (1) records who owns it, (2) can safely recover from stale/abandoned locks, (3) only reclaims/cleans up when ownership is verified, and (4) prevents partial/inconsistent state.

Apply this checklist:
- Use a dedicated lock location tied to a canonical resource path (e.g., make any configurable install-dir absolute before constructing the lock path).
- Store owner metadata inside the lock (at minimum: PID + process start time; use a stable timezone like UTC).
- On contention: wait with bounded retries/backoff.
- On suspected staleness: reclaim only after verifying the owner process is gone or has exceeded a grace period; for abandoned/partially initialized locks, recover only when safe.
- Never allow a contender to reclaim a successor lock: any recovery path must re-check the lock’s current owner metadata before proceeding.
- Use signal-safe cleanup (EXIT/INT/TERM) that removes temporary artifacts and deletes the lock only if you still own it.
- Ensure the critical operation writes atomically from a temporary location (so other processes never observe partially downloaded/partially installed state).

Example pattern (shell-style):
```bash
set -euo pipefail
lock_dir="${RESOURCE_DIR%/}/.install-lock"
mkdir -p "$RESOURCE_DIR"
owner="$ $ (TZ=UTC ps -p $$ -o lstart=)"  # PID + UTC start time (format as in your environment)

cleanup() {
  # Only delete if still owned
  if [[ -f "$lock_dir/owner" ]] && grep -Fxq "$owner" "$lock_dir/owner" 2>/dev/null; then
    rm -rf "$tmp" 2>/dev/null || true
    rm -rf "$lock_dir" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# Acquire (serialize)
for ((i=0; ; i++)); do
  if mkdir "$lock_dir" 2>/dev/null; then
    printf '%s
' "$owner" > "$lock_dir/owner"
    break
  fi
  # Stale detection (verify owner process/start time or grace period)
  # If stale: attempt reclaim but re-check ownership after reclaim
  sleep 0.5
  [[ $i -lt 240 ]] || { echo "lock held too long" >&2; exit 1; }
done

# Critical section: download/build into $tmp, then install atomically
```

This standard eliminates race conditions, prevents corruption from partially completed work, and makes concurrent automation reliable across multiple clients/sessions.