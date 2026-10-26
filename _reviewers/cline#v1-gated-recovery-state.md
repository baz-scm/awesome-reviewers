---
title: Gated Recovery State
description: In UI flows with async work or uncertain delivery, handle errors by making
  state transitions and recovery actions conditional on confirmed outcomes—and by
  ensuring deterministic cleanup/retry when events or requests don’t complete.
repository: cline/cline#v1
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70862
---

In UI flows with async work or uncertain delivery, handle errors by making state transitions and recovery actions conditional on confirmed outcomes—and by ensuring deterministic cleanup/retry when events or requests don’t complete.

Apply this standard:
- Gate user-visible mutations on success signals: only clear/reset state (e.g., commit message, drafts, optimistic UI) after the action reports success.
- Treat missing/failed recovery data as “unknown,” not “safe to restore”: only restore drafts/UI when you can determine the original content wasn’t delivered; otherwise, degrade gracefully (e.g., suppress restoration or require explicit user action).
- Provide retry points for recoverable failures: rerun initial lookups/recovery when the underlying transport reconnects (or on other replay-safe triggers), not only once at startup.
- Ensure deterministic cleanup for aborted interactions: if expected terminal events might not fire (e.g., `pointerup` outside window), make handlers self-terminate on observable abort conditions and always restore listeners/styles.

Example pattern (success-gated state update):
```ts
const commit = useCallback(async () => {
  const ok = await onAction({ type: "commit", message: message.trim(), push });
  if (ok) setMessage(""); // only clear on confirmed success
  // else keep message so user can retry/fix errors
}, [message, onAction]);
```

Example pattern (conditional restoration on uncertain delivery):
```ts
const saved = await refreshFollowUp().catch(() => undefined);
const canRestore = definitelyUndispatched || (canRestoreWhenEvidenceMatches(saved));
if (deliveryFailed && canRestore) restorePrompt();
// otherwise suppress restoration to avoid reintroducing already-edited/delivered content
```

Example pattern (retry lookup on reconnect):
```ts
useEffect(() => {
  desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then(setUrl, () => undefined);
}, [transportConnectedState]); // reconnect triggers recovery
```

Outcome: fewer stuck interactions, correct UI state after failures, and safer recovery that doesn’t violate the user’s intent when delivery/recovery evidence is incomplete.