---
title: Lock and Retry Rules
description: When coordinating async work with shared resources, (1) tie lock/flag
  state transitions to the real lifecycle of the work (e.g., confirmed detached handoff
  or confirmed error) rather than to generic function scope, and (2) treat resource
  contention as transient by using bounded retry + backoff for cleanup/claims.
repository: nousresearch/hermes-agent
label: Concurrency
language: Other
comments_count: 2
repository_stars: 221948
---

When coordinating async work with shared resources, (1) tie lock/flag state transitions to the real lifecycle of the work (e.g., confirmed detached handoff or confirmed error) rather than to generic function scope, and (2) treat resource contention as transient by using bounded retry + backoff for cleanup/claims.

Apply this in two parts:

1) Lock lifecycle: clear only when it’s actually safe
- Avoid clearing “in-flight” flags in `finally` if the process/work continues after the function returns (especially across deliberate dwell/shutdown delays). A `finally` can create a race window where another updater/retry can start.
- Ensure every non-throwing return path has an explicit, intended lock outcome: keep the lock only while the handoff/detached updater is expected to be alive; clear it for non-handoff outcomes; clear it on thrown errors.

Example pattern (JS):
```js
async function applyUpdates(opts = {}) {
  // ... acquire lock: updateInFlight = true
  try {
    const { ok, handedOff, updater } = await applyUpdatesPosixInApp();

    if (handedOff) {
      // Keep lock through quit dwell; do NOT clear via finally.
      return { ok, handedOff: true, updater };
    }

    // Non-handoff normal returns should release the lock.
    updateInFlight = false;
    return { ok, handedOff: false };
  } catch (err) {
    // Only on error: allow a retry by clearing lock.
    updateInFlight = false;
    throw err;
  }
}
```

2) Transient contention: bounded retry with backoff
- When deleting/renaming files or directories that may still be held by a just-killed/terminating process, assume handles may release slightly later.
- Implement a retry loop with exponential (or increasing) delays, and a clear upper bound after which the operation fails loudly.
- Don’t base correctness solely on disabling other systems (e.g., scheduled tasks) unless you also guard against an external watchdog continuing the contention.

Example pattern (PowerShell):
```powershell
# Attempt in-place delete with retries for transient file locks
Remove-Item -Recurse -Force 'venv' -ErrorAction SilentlyContinue
$retryDelay = 2
for ($retry = 0; $retry -lt 3; $retry++) {
  if (-not (Test-Path 'venv')) { break }
  Write-Info "venv still locked (attempt $($retry + 1)/3); waiting ${retryDelay}s..."
  Start-Sleep -Seconds $retryDelay
  $retryDelay *= 2
}
```

Net effect: you prevent race windows from premature lock clearing and you make cleanup operations resilient to short-lived contention—both are essential in concurrent and lifecycle-sensitive code.