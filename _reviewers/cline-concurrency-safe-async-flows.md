---
title: Concurrency-safe Async Flows
description: 'When implementing async/concurrent behavior, prevent stale updates,
  duplicate side-effects, and resource leaks by following these rules:


  1) Register wiring once; route through mutable state'
repository: cline/CLINE
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 70839
---

When implementing async/concurrent behavior, prevent stale updates, duplicate side-effects, and resource leaks by following these rules:

1) Register wiring once; route through mutable state
- Don’t attach handlers per retry/spawn attempt.
- Register listeners once, then enable/disable them via a mutable “slot” that retries update.

2) Supersede correctly across awaits
- If an async operation can be invalidated (tab closed, request stale, rebuild replaced), use a generation/token/currentness check.
- After each await (or before side-effects), verify the operation is still current.

3) Claim shared state before awaiting
- If multiple submissions can target the same “pending” resolver, synchronously claim/clear the resolver before any awaited work (e.g., attachment delivery) so another submission can’t resolve the same promise mid-flight.

4) Don’t re-discover mutable targets later
- If you need to update a specific entity (message index, record id), compute the target synchronously and capture it before starting the async/slow work.
- Avoid: “await slow commit, then find the newest checkpoint_created message.”

5) Serialize dependent workflows with a queue/scheduler
- Polling + actions, or rebuilds triggered during transitions, must join in-flight work and queue exactly one “latest” rerun per policy.
- Same-reason rebuild requests must supersede active runs (not just coalesce in the queue).

6) Cleanup resources once the promise settles
- On resolve/reject, remove listeners and release inherited handles (stdio pipes, timers, event listeners) so background children/callbacks can’t keep the process alive or accumulate output.

Example patterns

A) Listener registered once; mutable slot routes data
```ts
// register once
term.onData((data) => tab.pty?.write(data));
term.onResize(({ cols, rows }) => tab.pty?.resize(cols, rows));

// later, spawn toggles tab.pty / status
async function spawn(tab: TerminalTab) {
  if (tab.status !== "new") return;
  tab.status = "starting";
  tab.pty = { write: () => {/* invoke hub */}, resize: () => {/* invoke */} };
  try {
    await doSpawn();
    if (tab.status !== "starting") return; // invalidated during await
    tab.status = "running";
  } catch {
    tab.status = "exited";
    tab.pty = null;
  }
}
```

B) Claim pending resolver before awaiting delivery
```ts
const resolve = pendingAskResolve;
if (!resolve) return false;
pendingAskResolve = undefined; // claim immediately

const hasAttachments = images?.length || files?.length;
if (hasAttachments && deliverAttachments) {
  await deliverAttachments(() => /* still current */ true);
  // core will echo/handle; don’t allow another resolve
}
setPhase("streaming");
resolve(prompt ?? "");
return true;
```

C) Capture the exact target before slow async work
```ts
const idx = findLastIndex(messages, m => m.say === "checkpoint_created");
await say("checkpoint_created");
const targetIdx = idx; // capture synchronously after message is created
const commitHash = await checkpointTracker.commit();
if (commitHash && targetIdx !== -1) {
  await updateClineMessage(targetIdx, { lastCheckpointHash: commitHash });
}
```

Use this checklist during review: if a feature involves retries, cancellation, replacement, background tasks, polling+actions, or multi-client state, explicitly document how you prevent (1) duplicate side-effects, (2) stale writes after await, and (3) leaked resources after settlement.