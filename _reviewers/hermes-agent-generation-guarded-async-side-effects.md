---
title: Generation-guarded async side effects
description: When async work can overlap (navigation changes, optimistic updates,
  multiple handler invocations, or speech interruption), treat post-`await` mutations
  as conditional on the original intent. Capture (1) the state/identity you’re operating
  on and (2) a monotonically increasing generation/token before any `await` or long-running
  step. Only apply...
repository: nousresearch/hermes-agent
label: Concurrency
language: TypeScript
comments_count: 6
repository_stars: 221948
---

When async work can overlap (navigation changes, optimistic updates, multiple handler invocations, or speech interruption), treat post-`await` mutations as conditional on the original intent. Capture (1) the state/identity you’re operating on and (2) a monotonically increasing generation/token before any `await` or long-running step. Only apply success/failure/rollback when the token still matches the latest value; otherwise discard the completion.

Also, ensure that “normal completion” paths (e.g., a `finally` that re-arms listening) are skipped when an interrupt/cancel occurred; guard them with the same interruption flag/token.

Practical pattern:
```ts
let refreshGen = 0

async function refresh() {
  const gen = ++refreshGen
  const requestedBoard = $kanbanActiveBoard.get() // identity snapshot

  try {
    const next = await getKanbanBoard(requestedBoard)

    // Discard stale response
    if (gen !== refreshGen) return

    $kanbanBoard.set(next)
  } catch (e) {
    if (gen !== refreshGen) return
    $kanbanBoardError.set(String(e))
  }
}

async function moveOptimistic(taskId: string, targetStatus: string) {
  const gen = ++moveGen
  const boardAtStart = $kanbanBoard.get() // snapshot identity

  $kanbanBoard.set(applyMove(boardAtStart, taskId, targetStatus))

  try {
    await updateKanbanTask(taskId, { status: targetStatus }, $kanbanActiveBoard.get())
    if (gen !== moveGen) return
    await refreshFromServer(boardAtStart)
  } catch (e) {
    if (gen !== moveGen) return
    $kanbanBoard.set(boardAtStart) // guarded rollback
    $kanbanBoardError.set(parseError(e))
  }
}
```

Apply this rule whenever:
- the user can change selection/navigation while the request is in flight,
- multiple invocations of an async handler can race,
- you optimistically mutate shared state and later reconcile/rollback,
- a cancellation/interrupt can trigger `finally`/completion handlers that would otherwise perform the wrong re-arming behavior,
- concurrent mic/recorder resources must be reset on session switches.

Result: late/stale completions stop overwriting newer intent, and both success and error paths become race-safe.