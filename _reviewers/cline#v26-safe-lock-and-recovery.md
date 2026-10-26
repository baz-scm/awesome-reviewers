---
title: Safe lock and recovery
description: 'When multiple processes may touch the same install directory or resource,
  treat the critical section as a race: use filesystem locks that (1) are scoped deterministically,
  (2) record owner identity, (3) reclaim only truly abandoned locks, and (4) clean
  up only what you own.'
repository: cline/cline#v26
label: Concurrency
language: Shell
comments_count: 2
repository_stars: 70893
---

When multiple processes may touch the same install directory or resource, treat the critical section as a race: use filesystem locks that (1) are scoped deterministically, (2) record owner identity, (3) reclaim only truly abandoned locks, and (4) clean up only what you own.

Apply these rules:
- **Lock scope must be unambiguous:** convert any directory used in the lock path (e.g., `--install-dir`) to an **absolute path** before constructing `.../.install-lock`.
- **Record ownership robustly:** store **PID + UTC process start time** (not just PID) in the lock so stale PID reuse can’t fool you.
- **Reclaim only when safe:** a contender may reclaim only if the recorded owner is proven gone/changed (PID dead OR start time mismatch) or the lock is clearly abandoned after a grace window.
- **Recovery must be two-phase:** if you reclaim/reset inside a recovery subshell, **recheck the lock owner after the reclaim step** to ensure you don’t steal a successor lock.
- **Cleanup must be ownership-aware:** install/uninstall scripts should trap `EXIT/INT/TERM` and delete **temporary downloads/artifacts**, and remove the lock **only if you still own it**.

Illustrative pattern (shell):
```bash
install_dir="$(cd "$install_dir" 2>/dev/null && pwd)"  # ensure deterministic lock scope
lock="$install_dir/.install-lock"
owner="$$ $(TZ=UTC ps -p $$ -o lstart=)"

# try acquire
if mkdir "$lock" 2>/dev/null; then
  printf '%s
' "$owner" > "$lock/owner"
else
  # read previous owner and reclaim only if owner is dead/changed
  previous="$(cat "$lock/owner" 2>/dev/null || true)"
  prev_pid=${previous%% *}
  prev_start="${previous#* }"

  prev_alive=false
  if [[ "$prev_pid" =~ ^[0-9]+$ ]]; then
    cur_start="$(TZ=UTC ps -p "$prev_pid" -o lstart= 2>/dev/null || true)"
    [[ "$cur_start" == "$prev_start" ]] && prev_alive=true
  fi

  if [[ "$prev_alive" == false ]]; then
    # recovery: claim then recheck
    # (perform cleanup/reuse work here)
    # then verify lock owner is still the expected one before proceeding
  else
    echo "Another installer is running" >&2
    exit 1
  fi
fi

cleanup() {
  # remove only if still owner; otherwise don’t touch successor lock
  current_owner="$(cat "$lock/owner" 2>/dev/null || true)"
  [[ "$current_owner" == "$owner" ]] && rm -rf "$lock"
  rm -rf "$temporary"
}
trap cleanup EXIT INT TERM
```
This standard prevents race-induced partial installs, avoids accidental lock stomping, and ensures robust behavior under concurrent desktop/SSH/automation scenarios.