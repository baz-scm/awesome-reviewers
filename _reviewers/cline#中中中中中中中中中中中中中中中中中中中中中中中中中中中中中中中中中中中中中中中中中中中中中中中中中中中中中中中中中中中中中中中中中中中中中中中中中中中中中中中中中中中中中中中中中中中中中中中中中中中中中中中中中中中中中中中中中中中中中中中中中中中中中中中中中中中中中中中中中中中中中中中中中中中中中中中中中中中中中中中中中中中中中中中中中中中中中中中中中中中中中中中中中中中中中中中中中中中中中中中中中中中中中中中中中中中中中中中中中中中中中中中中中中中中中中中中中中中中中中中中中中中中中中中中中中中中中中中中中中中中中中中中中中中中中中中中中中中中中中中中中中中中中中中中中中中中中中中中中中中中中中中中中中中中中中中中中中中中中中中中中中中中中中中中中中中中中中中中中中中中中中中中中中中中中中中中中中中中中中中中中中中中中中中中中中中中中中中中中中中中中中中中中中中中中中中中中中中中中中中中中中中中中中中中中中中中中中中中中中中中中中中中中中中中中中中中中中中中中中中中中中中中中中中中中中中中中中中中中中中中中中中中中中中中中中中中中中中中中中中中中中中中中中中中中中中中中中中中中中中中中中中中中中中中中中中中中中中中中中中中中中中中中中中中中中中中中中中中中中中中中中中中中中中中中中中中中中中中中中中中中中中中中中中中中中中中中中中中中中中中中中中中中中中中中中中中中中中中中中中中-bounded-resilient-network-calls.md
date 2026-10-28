---
title: Bounded, resilient network calls
description: 'Every outbound network operation must be explicitly bounded and must
  not trust untrusted signals when deciding how to behave:


  1. **Always set a request timeout.** Any `fetch`/socket call that can reach a remote
  or unreliable host (including fallback code paths) needs an `AbortSignal`/timeout,
  not just the primary call. A host that drops packets instead of...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70984
---

Every outbound network operation must be explicitly bounded and must not trust untrusted signals when deciding how to behave:

1. **Always set a request timeout.** Any `fetch`/socket call that can reach a remote or unreliable host (including fallback code paths) needs an `AbortSignal`/timeout, not just the primary call. A host that drops packets instead of refusing a connection will hang forever without one, blocking the whole flow (e.g. task start).

2. **Never trust declared sizes.** Don't gate size limits on headers like `Content-Length`; a missing or incorrect header lets an attacker or misbehaving server force unbounded buffering. Stream the response and cancel as soon as the actually-received byte count crosses the limit.

3. **Classify addresses with a real IP parser, not ad-hoc string checks.** Loopback/private-network/proxy-bypass decisions must handle edge cases such as `0.0.0.0`, and IPv4-mapped IPv6 (`::ffff:127.0.0.1`). Use something like Node's `net.BlockList`, which matches mapped addresses against the IPv4 rules, instead of hand-rolled regex/prefix checks that silently miss these forms and fall back to the wrong timeout/proxy behavior.

4. **Treat transient network slowness as retryable, not fatal.** On a timeout, prefer a bounded health probe (e.g. a cheap coalesced "ping" command) before tearing down a connection/transport. Only retire the connection if the probe itself fails with no intervening successful traffic; never replay in-flight writes/prompts when recovering.

Example:
```ts
// Bad: no timeout, trusts Content-Length
const res = await fetch(url);
const body = Buffer.from(await res.arrayBuffer());

// Good: bounded timeout, enforced streaming limit
const res = await fetch(url, { signal: AbortSignal.timeout(timeoutMs) });
const reader = res.body.getReader();
let total = 0;
for (;;) {
  const { done, value } = await reader.read();
  if (done) break;
  total += value.length;
  if (total > maxBytes) { reader.cancel(); throw new Error("too large"); }
}

// Good: robust loopback/local detection
const local = new BlockList();
local.addSubnet("127.0.0.0", 8, "ipv4");
local.addAddress("0.0.0.0", "ipv4");
local.addAddress("::1", "ipv6");
// BlockList also matches "::ffff:127.0.0.1" against the ipv4 rule.
```

Applying these rules prevents hung tasks, resource-exhaustion from oversized downloads, misrouted/mis-timed-out local-server requests, and premature connection teardown on brief network hiccups.