---
title: Ground-truth error recovery
description: When recovering from a failed async operation, resync to the authoritative
  source of truth instead of guessing, pattern-matching, or replaying client-side
  assumptions. Fragile heuristics (parsing error strings, restoring a locally-captured
  "previous" value, retrying on an unrelated event) break under retries, races, or
  edge cases that weren't anticipated.
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 71067
---

When recovering from a failed async operation, resync to the authoritative source of truth instead of guessing, pattern-matching, or replaying client-side assumptions. Fragile heuristics (parsing error strings, restoring a locally-captured "previous" value, retrying on an unrelated event) break under retries, races, or edge cases that weren't anticipated.

- Determine failure/success from an explicit, deterministic check against real state (e.g., check the upstream ref `@{u}` directly instead of pattern-matching a push error message; re-run a lookup whenever the actual dependency it relies on reconnects, not on some loosely related event).
- On a failed optimistic update, roll the UI back to the backend/runtime's actual current state rather than to a captured "previous" value, since concurrent operations can make that captured value stale.
- Before applying a recovery/restoration action (especially a destructive one, like overwriting user input), distinguish definitely-failed operations from ones where the outcome is uncertain; only recover when you can prove the operation never took effect.

Example:
```ts
// Bad: restores a guessed previous value, which can be stale after rapid retries
props.onModeChange(newMode).catch(() => session.setUiMode(previousMode));

// Good: resync to the runtime's actual (ground-truth) state after a failure
props.onModeChange(newMode).catch((error) => {
  session.setUiMode(props.config.mode); // authoritative, not a guess
  reportError(error);
});
```
</description>
