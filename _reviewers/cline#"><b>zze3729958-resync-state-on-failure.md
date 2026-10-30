---
title: Resync state on failure
description: When an action triggers an async operation that can fail (mode switches,
  session resumes/detaches, draft restoration, push/retry logic), avoid committing
  optimistic or destructive state changes before the operation is confirmed successful.
  If the operation fails, roll back to the previous state and resync from the authoritative
  source of truth rather than...
repository: cline/cline#"><b>zze3729958
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 71067
---

When an action triggers an async operation that can fail (mode switches, session resumes/detaches, draft restoration, push/retry logic), avoid committing optimistic or destructive state changes before the operation is confirmed successful. If the operation fails, roll back to the previous state and resync from the authoritative source of truth rather than from a value captured before the attempt, so the UI never diverges from the real backend/runtime state.

Concretely:
- Detach/replace resources (e.g., a cloud session) only after the replacement/local action has succeeded, not before, so a failed operation leaves the original resource intact and usable.
- For toggles or mode changes that restart underlying state, catch the failure, revert the local state to the previous value, and re-sync from the canonical source (e.g., `props.config.mode`) instead of trusting a locally captured variable, to avoid UI/runtime mismatches.
- When deciding whether to recover or restore user input after a failed send, distinguish between "definitely not dispatched" and "uncertain delivery" — only auto-restore in the former case to avoid silently discarding edits or duplicating sends.
- Prefer checking explicit, authoritative state (e.g., upstream branch existence via `@{u}`) over inferring failure conditions by pattern-matching error messages, which is fragile and can silently produce wrong recovery behavior.
- Tie retry/recovery triggers to the signal that actually caused the failure (e.g., retry on transport reconnect, not on an unrelated refresh), so transient errors self-heal correctly.

Example pattern for safe rollback on async failure:
```ts
const toggleMode = useCallback(() => {
  const previousMode = session.uiMode;
  const newMode = previousMode === "act" ? "plan" : "act";
  session.toggleMode();
  props.onModeChange(newMode).catch((error: unknown) => {
    // Runtime restart failed; revert UI and restore prior config
    session.setUiMode(previousMode);
    applyInteractiveModeConfig(previousMode);
    showToast(`Failed to switch mode: ${error}`);
  });
}, [props, session]);
```
Applying this consistently prevents inconsistent UI/state after partial failures and makes error recovery predictable and testable (e.g., "a failed restart after applyMode('plan') leaves config.mode === 'act'").</description>
