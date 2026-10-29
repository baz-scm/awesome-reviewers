---
title: Graceful failure recovery
description: 'When an operation can fail, design the surrounding logic so failures
  degrade gracefully instead of corrupting state or crashing the app:


  1. Sequence side effects by success, not by intent. If an action depends on another
  operation succeeding (e.g. detaching a cloud session only makes sense if the local
  resume succeeds), perform the dependent/irreversible...'
repository: cline/cline#1
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 71024
---

When an operation can fail, design the surrounding logic so failures degrade gracefully instead of corrupting state or crashing the app:

1. Sequence side effects by success, not by intent. If an action depends on another operation succeeding (e.g. detaching a cloud session only makes sense if the local resume succeeds), perform the dependent/irreversible step only after the prerequisite has actually succeeded. Don't optimistically mutate state before confirming the operation it depends on worked, or a failure will leave the system in a broken, unrecoverable state.

2. Tie retries to the real failure/recovery trigger. One-shot requests made on mount (e.g. fetching a value from a sidecar on initial render) can fail transiently and then never be retried, permanently breaking a feature until a full restart. Attach the retry to the event that actually indicates recovery is possible (e.g., transport reconnect) rather than an unrelated lifecycle event, and add a test that simulates failure-then-recovery to confirm the retry path works.

3. For non-critical, fire-and-forget side effects (such as opening an external link), swallow failures explicitly with a no-op catch so an unavailable system resource (e.g. no browser opener) doesn't produce an unhandled rejection or crash the surrounding UI:
```ts
void open(url, { wait: false }).catch(() => {});
```
This keeps the primary flow (e.g., a dialog) usable even when the secondary action fails. Richer error UX (showing an error state, offering a fallback) can be added later, but silent failure must never be a hard crash or an unhandled rejection.

Applying these practices ensures failure scenarios are isolated, recoverable, and don't propagate into corrupted application state or unhandled exceptions.