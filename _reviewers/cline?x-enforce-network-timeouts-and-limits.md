---
title: Enforce network timeouts and limits
description: 'Every network call must have an explicit, enforced deadline and resource
  limit — never rely on a remote server, a host-supplied callback, or a default library
  setting to behave cooperatively. Concretely:'
repository: cline/cline?x
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70983
---

Every network call must have an explicit, enforced deadline and resource limit — never rely on a remote server, a host-supplied callback, or a default library setting to behave cooperatively. Concretely:

- Add a hard timeout/deadline to every outbound request, including rarely-hit fallback paths. A request that falls back to a secondary code path (e.g. a second fetch when the primary API fails) must carry the same timeout discipline as the primary one; otherwise a slow/unresponsive host can hang task startup or UI flows that users expect to fail fast.
- When a caller passes in an external callback (e.g. a host-supplied `fetch`), don't assume it respects `AbortSignal`. Wrap it with an independent timer/deadline so a buggy or malicious callback can't hang your code indefinitely.
- Enforce size/byte limits against data actually received, not against headers like `Content-Length`, which can be missing, wrong, or attacker-controlled. Stream/read incrementally and abort as soon as the running total exceeds the limit.
- For logic that classifies destinations for timeout or proxy policy (e.g. "is this address local/loopback so we should disable idle timeouts or bypass the proxy"), cover all equivalent forms of the address (`0.0.0.0`, IPv4-mapped IPv6 like `::ffff:127.0.0.1`, etc.) and add regression tests that exercise both the bypass and non-bypass branches with realistic proxy/env configuration.
- For stateful protocols with retries/reconnects (hub clients, websockets), tie timeout/deadline clearing to the specific request or run it protects, and make sure any live evidence (replies, heartbeats, terminal events) can clear it — but never let a missed signal cause a request to hang forever or get silently replayed.

Example of a defensive timeout wrapper for an externally supplied request function:

```ts
async function withTimeout<T>(
  run: (signal: AbortSignal) => Promise<T>,
  timeoutMs: number,
): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await run(controller.signal);
  } finally {
    clearTimeout(timer);
  }
}
```

Applying this consistently prevents silent hangs, unbounded memory growth, and inconsistent behavior between primary and fallback network paths.</description>
</invoke>
