---
title: Network retry and bounds
description: 'Define networking behavior so failures don’t cause duplicate work, hangs,
  or incorrect routing.


  Apply these rules:

  1) Track dispatch boundaries for retry/resend UX'
repository: CLINE/CLINE
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70837
---

Define networking behavior so failures don’t cause duplicate work, hangs, or incorrect routing.

Apply these rules:
1) Track dispatch boundaries for retry/resend UX
- If a failure happens after the request may already have been dispatched, the client must not treat it as “unsent” and must not offer a resend that could duplicate side effects.
- Prefer a Hub/transport API that returns typed failures including a `dispatched` (or equivalent) signal, and only surface “resend” for confirmed pre-dispatch failures.

2) Ensure every network path is bounded/abortable
- Not just the primary request: fallback discovery paths and alternate fetches must also use the same timeout/AbortSignal.

3) Make disconnect/reconnect semantics explicit
- On socket disconnect, define whether pending operations are cancelled immediately or preserved under a reconnect grace window; if preserved, cancel only on grace expiry.
- Do not implicitly re-execute callbacks or callbacks that may run twice.

4) Preserve correct proxy + loopback behavior when customizing HTTP dispatchers
- When disabling timeouts/idle behavior or using custom agents/dispatchers, keep loopback routing consistent with the existing resolver behavior.
- Ensure “local server” detection includes common variants like `0.0.0.0` and IPv4-mapped loopback (`::ffff:127.0.0.1`).

Example patterns:

A) Avoid duplicate resend after dispatch
```ts
type SendFailure = { dispatched: boolean; kind: "pre_dispatch" | "post_dispatch"; /* ... */ };

function uiResendAllowed(err: SendFailure) {
  // Only allow resend when we know it was never dispatched.
  return err.dispatched === false && err.kind === "pre_dispatch";
}
```

B) Abort fallback fetches too
```ts
async function fetchModelIdsFromSource(url: string, signal: AbortSignal) {
  const res = await fetch(url, { signal });
  // ...
}
```

Checklist for PRs touching networking
- Does the code path that can fail determine whether it was dispatched? If yes, is the UI behavior consistent with that?
- Do all fetch/WebSocket/stream operations accept and honor AbortSignal and timeouts (including fallbacks)?
- On disconnect, are pending operations cancelled/preserved with a clearly documented policy (and no callback re-execution)?
- If you change HTTP agents/dispatchers, do loopback and local-server routing still work with proxy env vars (and are `0.0.0.0` / mapped IPv4 covered)?
