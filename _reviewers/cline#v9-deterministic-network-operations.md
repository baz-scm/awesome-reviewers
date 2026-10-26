---
title: Deterministic Network Operations
description: Network code must be deterministic about (a) routing (proxy vs loopback/local),
  (b) cancellation/time bounds, and (c) connection/dispatch state—so errors don’t
  turn into hangs, background connects, or double-sends.
repository: cline/cline#v9
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70868
---

Network code must be deterministic about (a) routing (proxy vs loopback/local), (b) cancellation/time bounds, and (c) connection/dispatch state—so errors don’t turn into hangs, background connects, or double-sends.

**Standards**
1. **Always bound and abort every request path**
   - If you add a timeout/AbortSignal to a primary call, apply the same cancellation to *fallbacks* and any secondary fetches.
   - Ensure task-start/critical flows can’t hang indefinitely due to an unbounded fallback.

2. **Preserve loopback semantics when using proxy-aware agents**
   - If your platform previously connected directly to `127.0.0.1`/`::1`, do not route loopback through `HTTP_PROXY` when `NO_PROXY` is unset.
   - Add a regression test that runs with `HTTP_PROXY` set and `NO_PROXY` unset.

3. **Correctly classify “local network” targets**
   - Your “local model server” detection must include common real-world bind addresses like `0.0.0.0` and IPv4-mapped loopback (e.g. `::ffff:127.0.0.1`) so the correct fetch strategy is chosen.

4. **Model connection/readiness and send dispatch boundaries explicitly**
   - For read operations over a hub/transport link: don’t immediately fail while the link is still connecting—wait briefly and retry; return a defined state like `unknown` when the transport isn’t ready.
   - For write/send operations: the client must know whether the transport *dispatched* the send before failure. Only treat it as retryable if it was definitely not dispatched. Never rely on “failure occurred” to imply “nothing was sent.”

5. **Avoid unintended background network connections in UI hydration**
   - Do not implicitly open remote transports during sidebar/list hydration. Use persisted/discovery data, or gate remote reads behind explicit user/open events.

**Pattern (sketch)**
```ts
async function safeFetchJson<T>(url: string, init: RequestInit & { signal?: AbortSignal }) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);
  const signal = init.signal ?? controller.signal;

  try {
    // Choose an agent/fetch strategy based on local-vs-remote classification.
    const res = await fetch(url, { ...init, signal });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return (await res.json()) as T;
  } finally {
    clearTimeout(timeout);
  }
}

// Hub-like send: require dispatch confirmation from transport.
async function hubSendWithNoDoubleSend(sendFn: () => Promise<{ dispatched: boolean; error?: unknown }>) {
  const { dispatched, error } = await sendFn();
  if (error) {
    if (dispatched) {
      // Treat as “in-flight/unknown”; do not offer resend that could duplicate.
      return { kind: "unconfirmed" as const };
    }
    return { kind: "retryable" as const };
  }
  return { kind: "sent" as const };
}
```

Applying these rules prevents the common failures described above: proxy-induced loopback breakage, request hangs from unbounded fallbacks, and incorrect retry/resend behavior caused by missing dispatch/connection state.