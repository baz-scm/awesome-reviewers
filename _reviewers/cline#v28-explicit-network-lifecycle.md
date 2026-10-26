---
title: Explicit Network Lifecycle
description: Network operations must define the full lifecycle (readiness → retries/reconnects
  → cancellation/timeouts → routing), rather than failing fast or leaving unbounded
  fallbacks.
repository: cline/cline#v28
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70892
---

Network operations must define the full lifecycle (readiness → retries/reconnects → cancellation/timeouts → routing), rather than failing fast or leaving unbounded fallbacks.

Apply this when adding/changing network code:
- **Bound every path**: any fallback fetch, secondary endpoint, or “best-effort” call must have a timeout/AbortSignal wired through.
- **Handle “not ready” vs “failed”**: if a dependency may be connecting, use a **bounded wait** and/or a **retry** after reconnect instead of returning empty/unknown immediately.
- **Define reconnect grace for in-flight work**: decide whether pending requests survive transient disconnects; if so, keep the pending request until grace expiry, then cancel deterministically. Don’t silently cancel on the first disconnect.
- **Preserve correct routing under proxies**: when HTTP(S)_PROXY is set, ensure localhost/loopback routing semantics remain correct (avoid proxying loopback if your resolver/direct-routing behavior requires it).
- **Classify local vs remote deliberately**: if behavior differs for local model servers (e.g., disabling idle timeouts), use robust local-address detection (include common variants like `0.0.0.0`, IPv4-mapped loopback) and keep the proxy-aware behavior for remote targets.

Example pattern (wait+retry + bounded timeout with AbortSignal):
```ts
async function readWithReconnect(link: HubLink, sessionId: string, signal: AbortSignal) {
  // 1) Wait briefly for readiness
  await link.connected(5000, signal);

  // 2) Read, but retry once if the connection dropped
  try {
    const res = await link.command('session.messages', { sessionId }, { signal });
    return res;
  } catch (e) {
    await link.connected(5000, signal);
    return await link.command('session.messages', { sessionId }, { signal });
  }
}
```
This standard prevents empty/incorrect results during startup races, avoids hanging on unbounded fallbacks, and ensures network behavior stays correct under proxies and transient connectivity changes.