---
title: Enforce API Contracts
description: Client and UI code must explicitly follow the real API/component contract—both
  for *what state transitions are allowed* and *which side effects/transport paths
  are actually executed*.
repository: nousresearch/hermes-agent
label: API
language: TSX
comments_count: 3
repository_stars: 221948
---

Client and UI code must explicitly follow the real API/component contract—both for *what state transitions are allowed* and *which side effects/transport paths are actually executed*.

Apply this by:
- **Model allowed transitions from the backend**: only present or enable UI actions (e.g., drag/drop targets) that the backend will accept, or introduce an explicit “transition contract” endpoint/schema used by the client.
- **Force the intended integration path**: when a feature requires a specific transport (e.g., gateway API vs local filesystem/IPC), ensure the client has an explicit forced path and tests cover edge cases.
- **Don’t rely on “notification” callbacks for cancellation**: if you need to prevent a side effect/state change, intercept it *before* the underlying system commits state (use controlled state / pre-commit logic), rather than assuming an `onXChange`/callback can suppress the underlying action.

Example pattern for transition gating:
```ts
// pseudo: fetch/derive allowed destinations for the client
const allowed = await api.getAllowedKanbanTransitions(taskId)

function onDrop(toStatus: KanbanStatus) {
  if (!allowed.includes(toStatus)) return // backend will reject; avoid optimistic move

  // then call backend and update UI
  await api.updateKanbanTask(taskId, { status: toStatus })
  await refreshBoard()
}
```

Outcome: fewer “optimistic” failures, fewer integration drift bugs (wrong transport), and predictable behavior when APIs/components have non-cancelable lifecycle hooks.