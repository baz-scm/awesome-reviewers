---
title: Guard Async State Updates
description: When multiple async operations can be in flight (polling, optimistic
  mutations, React effects, REST hydration + live WebSocket deltas), older responses
  may arrive last and overwrite newer state. Standardize a pattern that makes each
  async result apply only if it is still the current/owned operation.
repository: nousresearch/hermes-agent
label: Concurrency
language: TSX
comments_count: 3
repository_stars: 221948
---

When multiple async operations can be in flight (polling, optimistic mutations, React effects, REST hydration + live WebSocket deltas), older responses may arrive last and overwrite newer state. Standardize a pattern that makes each async result apply only if it is still the current/owned operation.

Apply this rule:
- For any async function that calls `setState`, capture a “generation” (requestId) or “owner key” (e.g., selected board slug, active session id) and verify it before committing results.
- Ensure only one “owner” effect is responsible for a given resource at a time; otherwise explicitly cancel/ignore earlier requests.
- For hydrate-vs-stream scenarios, either (a) make hydrate generation-aware so it won’t clobber newer deltas, or (b) merge hydrate with subsequent deltas based on versions/timestamps.

Example pattern (generation-aware commit):
```ts
const requestGenRef = useRef(0)

const refresh = useCallback(async () => {
  const gen = ++requestGenRef.current
  try {
    const data = await getKanbanTasks()
    // Only the latest in-flight request may update state
    if (gen !== requestGenRef.current) return
    setTasks(Array.isArray(data.tasks) ? data.tasks : [])
  } catch (e) {
    if (gen !== requestGenRef.current) return
    notifyError(e)
  }
}, [])
```

Also guard by selection/ownership:
- Capture `selectedBoardSlug` (or session id) used to start the request, and before `set*`, verify it still matches the current value.

This prevents race-condition clobbering and makes state transitions deterministic under concurrency.