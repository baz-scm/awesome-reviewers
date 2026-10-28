---
title: Guard stale async callbacks
description: 'When a hook kicks off an async action (an API/IPC call, a promise race
  with a timeout, etc.), the component or data it closed over may change before the
  result arrives: the user navigates away and back, remounting the pane; a file or
  queued item is added/removed; another action resolves first; or persisted state
  merges in while a live update is still in...'
repository: 'cline/cline

  '
label: React
language: TypeScript
comments_count: 4
repository_stars: 70942
---

When a hook kicks off an async action (an API/IPC call, a promise race with a timeout, etc.), the component or data it closed over may change before the result arrives: the user navigates away and back, remounting the pane; a file or queued item is added/removed; another action resolves first; or persisted state merges in while a live update is still in flight. Never let the callback blindly apply its original assumptions once the await resolves — re-check what is actually true at that moment and reconcile against it.

Concretely:
- Snapshot only the inputs you truly need at invocation time (e.g. which attachments were present when Send was pressed), then re-derive the outcome from current state when the verdict lands (e.g. send only attachments still present, leave out anything removed meanwhile, keep anything added meanwhile).
- Track identity with a generation/binding ref (e.g. `boundRef`, `generationRef`) and bail out of applying a result if the binding changed while awaiting, instead of trusting a stale instance's ref/state after unmount or remount.
- Base "undo"/"restore" style continuations on the actual resolved outcome (e.g. "was this item actually removed, or did it already start, or neither?"), not on an assumption made before the await, and make repeated triggers (e.g. double-undo) no-ops while one is in flight.
- When merging transient/live state into canonical/persisted state, preserve ordering and de-duplicate by identity rather than overwriting.

Example pattern:
```ts
const boundId = boundRef.current;
const snapshot = takeSnapshotNeededForResult();
const result = await invoke(action);
if (boundRef.current !== boundId) return; // instance/binding changed, discard
applyReconciled(result, snapshot, currentLiveState());
```

Add regression tests that exercise the race explicitly (navigate away and back before the async result resolves, remove/add state while waiting, trigger the action twice) to lock in the reconciliation behavior.