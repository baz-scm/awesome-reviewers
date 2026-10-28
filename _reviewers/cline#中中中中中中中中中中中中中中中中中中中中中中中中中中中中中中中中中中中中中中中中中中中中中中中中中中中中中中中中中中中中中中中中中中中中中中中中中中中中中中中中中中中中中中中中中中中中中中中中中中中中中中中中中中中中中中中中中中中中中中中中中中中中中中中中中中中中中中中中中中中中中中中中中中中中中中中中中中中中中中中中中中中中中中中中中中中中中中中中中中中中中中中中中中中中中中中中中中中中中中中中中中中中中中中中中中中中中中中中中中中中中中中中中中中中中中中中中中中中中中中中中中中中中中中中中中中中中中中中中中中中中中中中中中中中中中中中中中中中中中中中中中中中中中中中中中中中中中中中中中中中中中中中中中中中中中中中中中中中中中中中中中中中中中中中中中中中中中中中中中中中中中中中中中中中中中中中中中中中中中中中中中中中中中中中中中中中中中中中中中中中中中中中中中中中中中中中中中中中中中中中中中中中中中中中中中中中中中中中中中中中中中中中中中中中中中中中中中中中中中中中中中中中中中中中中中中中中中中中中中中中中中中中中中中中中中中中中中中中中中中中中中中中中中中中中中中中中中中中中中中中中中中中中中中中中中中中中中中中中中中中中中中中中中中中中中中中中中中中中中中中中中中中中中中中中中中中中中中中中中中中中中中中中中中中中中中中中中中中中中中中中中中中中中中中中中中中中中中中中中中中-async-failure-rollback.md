---
title: Async failure rollback
description: 'When an async operation can fail, design its error path deliberately
  instead of letting failures propagate unchecked or state drift out of sync:


  1. **Defer irreversible side effects until success is confirmed.** Don''t detach,
  discard, or clear state optimistically before the dependent operation succeeds —
  e.g. detach a cloud session only after the local...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Error Handling
language: TSX
comments_count: 7
repository_stars: 70984
---

When an async operation can fail, design its error path deliberately instead of letting failures propagate unchecked or state drift out of sync:

1. **Defer irreversible side effects until success is confirmed.** Don't detach, discard, or clear state optimistically before the dependent operation succeeds — e.g. detach a cloud session only after the local resume actually succeeds, not before attempting it.
2. **Always handle rejections on fire-and-forget calls.** Attach a `.catch(() => {})` (or log) to any promise whose failure shouldn't crash the app or block the UI (e.g. opening an external link, quitting the app), but make sure this doesn't silently swallow errors that the user needs to see.
3. **Roll back to the authoritative state, not a stale captured value.** When reverting UI after a failed async action, resync from the current source of truth rather than a locally captured "previous" variable, so overlapping/racing failures all converge to the same correct state:
   ```ts
   props.onModeChange(newMode).catch((error) => {
     // Resync from the true config, not the captured previousMode,
     // so repeated failures don't disagree with each other.
     session.setUiMode(props.config.mode);
     showToast(describeError(error));
   });
   ```
4. **Pick the retry trigger that matches the actual dependency.** Recover failed lookups on the event that actually indicates recoverability (e.g. transport reconnect), not an unrelated signal (e.g. account refresh) that happens to fire nearby.
5. **Don't apply blanket recovery when the failure state is ambiguous.** Only auto-restore/recover when you can positively confirm the operation never took effect; if delivery/state is uncertain, treat it conservatively rather than assuming "failed" and overwriting potentially-delivered data.
6. When a failure mode is a fundamental platform limitation that can't be fully solved, document the limitation explicitly in code, keep a sane degraded fallback behavior, and note the long-term fix path rather than leaving it unexplained.</description>
