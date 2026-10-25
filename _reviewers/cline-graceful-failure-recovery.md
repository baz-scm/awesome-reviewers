---
title: Graceful Failure Recovery
description: 'When handling async actions, transport startup, or event-driven UI,
  treat failures and edge-case delivery as first-class: recover explicitly, preserve
  user input on failure, and always clean up global/UI state.'
repository: ClInE/cLiNe
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70838
---

When handling async actions, transport startup, or event-driven UI, treat failures and edge-case delivery as first-class: recover explicitly, preserve user input on failure, and always clean up global/UI state.

Apply these standards:
1) Clear/commit state only after confirmed success
- Don’t “optimistically” clear user inputs if the action may fail. Preserve input when the promise rejects or returns failure.

2) Replace—not just cover—UI on late failures
- If a critical dependency fails after an app has mounted (e.g., hub/sidecar), switch UI to an appropriate failure/startup screen by unmounting/replacing the prior tree. Covering can trap focus, disable pointer events, or leave stale layers.

3) Recover from timeouts by retrying on reconnect/transport changes
- For startup lookups that can fail or time out, bind recovery to the retry point (e.g., “transport connected again”), not to unrelated account refreshes.

4) Harden event flows for missing lifecycle events
- For drag/pointer interactions, assume pointerup may not fire (release outside window). Detect release via state (e.g., no button held) and then restore global styles/listeners.

Mini-pattern (success-gated state cleanup):
```ts
const commit = useCallback(async () => {
  const trimmed = message.trim();
  if (!trimmed || busy) return;

  const ok = await onAction({ type: "commit", message: trimmed, push: true });
  if (!ok) return; // keep message for user correction

  setMessage("");
}, [message, busy, onAction]);
```

Mini-pattern (retry lookup on reconnect):
```ts
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient.invoke<string>("get_cline_app_base_url")
    .then(setClineAppBaseUrl)
    .catch(() => undefined);
}, [transport]);
```

Mini-pattern (event cleanup on inferred release):
```ts
const handleMove = (move: PointerEvent) => {
  // If buttons state indicates release without pointerup delivery
  if (move.buttons === 0) { cleanupAndEndDrag(); return; }
  onHeightChange(clamp(...));
};
```