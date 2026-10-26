---
title: Network retries and routing
description: 'When implementing networking/reconnection logic, treat correctness as
  (1) lifecycle/dispatch boundaries and (2) routing/proxy selection.


  1) Prevent double execution across reconnects'
repository: cline/cline#v11
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70871
---

When implementing networking/reconnection logic, treat correctness as (1) lifecycle/dispatch boundaries and (2) routing/proxy selection.

1) Prevent double execution across reconnects
- Define an explicit “dispatch acknowledged” boundary in the transport/hub layer.
- On reconnect/retry, only resend work that was *not yet dispatched/leased*.
- If a request was dispatched, report failure as “dispatched” and never offer/attempt resend that would duplicate side effects.
- If a session/attach was withdrawn (detach/forget/dispose), ensure retries withdraw too (so the retry cannot re-lease after detach).
- Add tests for: transient “endpoint not ready”, lost replies, and “retry after connect” without double-sending.

Example pattern (conceptual):
```ts
// Hub/transport should return or emit whether dispatch happened
type SendResult = { dispatched: true } | { dispatched: false; error: unknown };

async function sendWithReconnect(...) {
  const result: SendResult = await hub.send(...);
  if (result.dispatched) {
    // do NOT replay on client retry
    return { kind: "dispatched_failed" };
  }
  // only safe-to-retry requests
  await retryOnce(...);
}
```

2) Preserve correct routing under proxies
- If you use a special fetch/agent (e.g., disabling idle timeouts), preserve the app’s existing loopback/direct-routing behavior even when `HTTP_PROXY` is set.
- Add/extend local-network address classification for common local bind targets (e.g., `127.0.0.0/8`, `10/8`, `172.16/12`, `169.254/16`, `100.64/10`, `::1`, plus operational cases like `0.0.0.0` and IPv4-mapped loopback).
- When switching agents based on “local vs remote”, ensure your tests set `HTTP_PROXY` and explicitly unset `NO_PROXY` to prevent regressions.

3) Keep network policy minimal and platform-correct
- Avoid enabling ingress/egress rules unless required; sandbox tiers may reject configurations that look permissive but break enforcement.

Use this checklist whenever touching networking, reconnects, proxy-aware fetch, or retry UX.