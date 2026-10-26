---
title: Bounded, idempotent networking
description: 'When you do network/IPC work, treat connection lifecycle as part of
  correctness:


  1) Bound every network call (including fallbacks)

  - Every fetch/request must have a timeout and an AbortSignal; never use a “bare
  fetch” in fallback code paths.'
repository: cline/cline#v23
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70889
---

When you do network/IPC work, treat connection lifecycle as part of correctness:

1) Bound every network call (including fallbacks)
- Every fetch/request must have a timeout and an AbortSignal; never use a “bare fetch” in fallback code paths.

2) Use short connection grace + limited retries for dependencies that may be starting
- If a target (e.g., hub/sidecar) is still connecting, wait briefly (and retry once after reconnect) instead of failing immediately with an empty/incorrect result.
- Distinguish “no running/disposed target” from “transient hub error reply”.

3) Make dispatch boundaries explicit to prevent duplicate side effects
- Clients must only offer “resend” (or retry-send) after confirming whether the request was already dispatched.
- Propagate typed failure that includes whether dispatch occurred; keep in-flight commands open across transient “endpoint not ready” until the safe send boundary or a deadline.

4) Enforce connect deadlines for in-flight operations
- If the connection never becomes ready, fail once after a deadline (don’t hang indefinitely).

5) Proxy-aware HTTP must preserve expected loopback routing
- When HTTP_PROXY/NO_PROXY environment variables exist, ensure localhost/loopback still uses direct routing if the system’s resolver expects it.
- Add regression tests covering proxy-on + NO_PROXY-unset with a loopback target.

Minimal example (timeout + abort, including fallback):
```ts
async function fetchWithTimeout(url: string, ms: number, signal?: AbortSignal) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(new Error("timeout")), ms);
  const combined = signal
    ? // AbortSignal.any not universally available; simplest pattern is to race
      (() => {
        const c = new AbortController();
        signal.addEventListener("abort", () => c.abort(signal.reason), { once: true });
        ctrl.signal.addEventListener("abort", () => c.abort(ctrl.signal.reason), { once: true });
        return c.signal;
      })()
    : ctrl.signal;

  try {
    return await fetch(url, { signal: combined });
  } finally {
    clearTimeout(t);
  }
}

// In fallback paths, reuse the same timeout/abort pattern.
```