---
title: Connection-boundary correctness
description: When implementing networking flows (HTTP, sockets, remote sessions),
  treat behavior as a function of explicit connection boundaries—don’t infer them
  from symptoms.
repository: cline/cline#v17
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70883
---

When implementing networking flows (HTTP, sockets, remote sessions), treat behavior as a function of explicit connection boundaries—don’t infer them from symptoms.

Apply this standard:
- **HTTP routing/proxy boundaries:** If you introduce custom HTTP behavior (timeouts, dispatcher changes, local-server fast paths), preserve the project’s intended routing rules (e.g., loopback must remain direct even when `HTTP_PROXY` is set). Add regression tests that set proxy env vars and validate localhost vs non-local behavior.
- **Socket/transport dispatch boundaries:** For send/retry logic over hubs/websockets, the transport layer must report whether a message crossed the dispatch boundary. Clients must only allow “resend” for **confirmed pre-dispatch** failures; otherwise they should surface a non-replayable error and handle reconciliation via connection recovery.
- **Remote connection policy boundaries:** When deciding whether edits are allowed for connected vs disconnected sessions, classify settings by whether a reconnect would fail identically through the new path (e.g., proxy reachability). Prefer consistency that prevents blocking valid cleanup/retry scenarios.

Sketch (HTTP boundary pattern):
```ts
// Pseudocode: route loopback directly; route others via proxy-aware agent
export const fetchWithoutIdleTimeouts: typeof fetch = (input, init) => {
  if (mockFetch) return mockFetch(input, init)
  const url = new URL(input.toString())
  const isLoopback = url.hostname === 'localhost' || isLoopbackIp(url.hostname)
  const dispatcher = isLoopback
    ? new Agent({ headersTimeout: 0, bodyTimeout: 0 })
    : new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 })
  return undiciFetch(input, { ...init, dispatcher })
}
```

Sketch (dispatch boundary pattern):
```ts
// Transport returns typed failure including whether it was dispatched
type SendFailure = { dispatched: false; unsentDraft: string } | { dispatched: true; error: Error }

function handleSendFailure(f: SendFailure) {
  if (!f.dispatched) {
    // safe to offer resend of unsent draft
  } else {
    // non-replayable; do not offer resend
  }
}
```

Net effect: fewer double-sends, fewer phantom retries, and correct behavior across proxies/local networks and connection drops—because the code depends on boundary signals you can test, not on guesswork from failure modes.