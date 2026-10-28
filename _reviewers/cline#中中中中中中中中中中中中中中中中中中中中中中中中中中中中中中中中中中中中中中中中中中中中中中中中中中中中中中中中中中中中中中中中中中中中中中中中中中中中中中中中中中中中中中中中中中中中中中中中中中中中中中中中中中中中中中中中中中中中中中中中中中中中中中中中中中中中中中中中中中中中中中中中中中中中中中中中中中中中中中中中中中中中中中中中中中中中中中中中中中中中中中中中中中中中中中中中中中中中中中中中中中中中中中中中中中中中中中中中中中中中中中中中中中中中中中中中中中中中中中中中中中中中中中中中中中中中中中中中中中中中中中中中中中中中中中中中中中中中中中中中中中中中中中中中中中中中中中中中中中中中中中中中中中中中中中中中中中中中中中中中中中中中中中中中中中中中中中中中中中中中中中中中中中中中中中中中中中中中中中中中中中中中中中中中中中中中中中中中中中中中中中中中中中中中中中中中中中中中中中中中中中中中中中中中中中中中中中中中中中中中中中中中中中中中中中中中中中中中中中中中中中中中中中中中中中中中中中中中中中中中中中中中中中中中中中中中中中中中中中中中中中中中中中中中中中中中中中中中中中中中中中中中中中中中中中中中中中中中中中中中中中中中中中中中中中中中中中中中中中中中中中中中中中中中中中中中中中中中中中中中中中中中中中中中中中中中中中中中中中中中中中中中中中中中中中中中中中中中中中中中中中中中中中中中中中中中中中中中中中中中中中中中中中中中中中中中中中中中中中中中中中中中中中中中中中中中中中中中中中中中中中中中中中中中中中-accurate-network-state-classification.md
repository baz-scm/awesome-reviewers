---
title: Accurate network state classification
description: When code branches on network state — local vs. remote endpoint, connected
  vs. disconnected client, slow vs. dead socket — enumerate every real-world representation
  of that state and verify the behavior matches existing, established routing rules
  elsewhere in the system. Add regression tests for the edge cases, not just the common
  case.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70986
---

When code branches on network state — local vs. remote endpoint, connected vs. disconnected client, slow vs. dead socket — enumerate every real-world representation of that state and verify the behavior matches existing, established routing rules elsewhere in the system. Add regression tests for the edge cases, not just the common case.

Concretely:
- Local-network/loopback detection must cover all address spellings: `0.0.0.0` (bind-all), IPv4-mapped IPv6 (`::ffff:127.0.0.1`), and the full private/link-local ranges — not just `127.0.0.1`/`::1`.
- Any custom fetch/transport path that bypasses a proxy agent (e.g. for long-idle local model servers) must preserve the host's pre-existing direct-routing rules, such as "loopback is always dialed directly, proxy env vars notwithstanding." Don't let a new code path silently reintroduce proxying for loopback just because the underlying HTTP client defaults to proxying everything when `HTTP_PROXY` is set and `NO_PROXY` is absent.
- Platform-specific network policies (e.g. sandbox ingress/egress rules) must only request capabilities actually needed; an unused loopback-ingress grant can cause an entire enforcement tier to reject the policy on some platforms (e.g. Windows AppContainer) even though it's harmless elsewhere (e.g. Linux namespaces).
- Before tearing down or retrying over a connection due to a timeout, confirm the transport is actually dead (e.g. via a coalesced health probe) rather than assuming a slow response means a dead socket — this avoids spurious reconnects/replays of writes.
- When resolving "which client/owner should handle this," check real liveness/attachment state (e.g. active session participants) rather than raw connection presence, so a client that disconnected-but-not-cleaned-up isn't selected.

Example pitfall and fix (local-network check):
```ts
// Before: misses 0.0.0.0 and IPv4-mapped IPv6
const LOCAL_NETWORK_ADDRESSES = new BlockList()
LOCAL_NETWORK_ADDRESSES.addSubnet("127.0.0.0", 8, "ipv4")
// ... missing 0.0.0.0/32 and ::ffff:0:0/96

// After: cover bind-all and mapped addresses explicitly
LOCAL_NETWORK_ADDRESSES.addSubnet("0.0.0.0", 32, "ipv4")
// BlockList.check already matches ::ffff: addresses against ipv4 rules,
// but add explicit tests for both spellings to lock in the behavior.
```

Treat these classification functions as security/correctness-critical: review them for every address format and connection-state transition a user could realistically hit, and cover each with a dedicated test.</description>
