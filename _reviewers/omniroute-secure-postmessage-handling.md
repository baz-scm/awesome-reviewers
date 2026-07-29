---
title: Secure postMessage handling
description: 'When handling cross-window `postMessage`, don’t rely on a single `window.location.origin`
  check—loopback flows (e.g., `localhost` vs `127.0.0.1`) can be legitimate but have
  different origins. For security, combine: (1) strict message type checking, (2)
  a whitelist of allowed origins that includes known legitimate loopback variants,
  and (3) a correlation ID...'
repository: diegosouzapw/OmniRoute
label: Security
language: TSX
comments_count: 1
repository_stars: 33162
---

When handling cross-window `postMessage`, don’t rely on a single `window.location.origin` check—loopback flows (e.g., `localhost` vs `127.0.0.1`) can be legitimate but have different origins. For security, combine: (1) strict message type checking, (2) a whitelist of allowed origins that includes known legitimate loopback variants, and (3) a correlation ID match (e.g., `loginTraceId`) to reject unsolicited/injected messages.

Example pattern:
```ts
const allowedOrigins = new Set([
  'http://localhost:3000',
  'http://127.0.0.1:3000',
]);
const expectedTraceId = traceIdRef.current;

function onMessage(ev: MessageEvent) {
  if (!allowedOrigins.has(ev.origin)) return;

  const m = ev.data as {
    type?: string;
    loginTraceId?: string;
    success?: boolean;
    error?: string;
  };

  if (m?.type !== 'trae-oauth-callback') return;
  if (expectedTraceId && m.loginTraceId !== expectedTraceId) return;

  // handle verified message
}
```

Apply this anywhere you parse `postMessage` for auth/callback flows: accept only known origins, verify the message shape/type, and require a per-attempt correlation token.