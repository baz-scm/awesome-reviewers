---
title: State-safe error handling
description: 'Treat failures/partial states as first-class: validate prerequisites
  up front, keep user/system state unchanged until an async action definitively succeeds,
  and make cleanup/recovery deterministic.'
repository: cline/cline#v6
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70864
---

Treat failures/partial states as first-class: validate prerequisites up front, keep user/system state unchanged until an async action definitively succeeds, and make cleanup/recovery deterministic.

Practical rules:
1) Gate side effects behind success
- If an operation can fail, don’t detach/commit-reset/clear inputs until the promise resolves successfully.
- On failure: preserve drafts, messages, and attachments; don’t leave the system in a “half switched” mode.

2) Reuse a single source of truth for precondition checks
- Before sending or mutating sessions, run the same checks the target composer/task uses (capabilities, read-only, supported inputs/models, required repo/model).
- When blocked, show the standard toast/feedback and do not mutate draft/attachments.

3) Guard by mode/environment to prevent invalid operations
- For cloud vs local tasks, disable or remove controls and refuse calls that the runtime can’t perform.
- If “Reset Chat”/edit should not run for cloud transcripts, prevent it instead of attempting and then correcting.

4) Ensure invariants even when events fail to arrive
- Assume UI events like pointerup/mouseleave may not fire (release outside window). Detect alternative termination conditions and restore listeners/body styles.

5) Add retry/recovery for transient dependency failures
- For startup/sidecar/websocket dependencies, retry based on transport/connection state changes and cover with tests.

Pattern example (side-effect only after success + preserve state on failure):
```ts
const [message, setMessage] = useState("");

async function commit(push: boolean) {
  if (message.trim().length === 0) return;
  const ok = await onAction({ type: "commit", message: message.trim(), push });
  if (!ok) return;           // keep message for retry
  setMessage("");           // only clear on confirmed success
}
```

Apply the same idea to other stateful transitions (e.g., only detach cloud sessions after local resume succeeds; only “reset” after the correct runtime confirms).