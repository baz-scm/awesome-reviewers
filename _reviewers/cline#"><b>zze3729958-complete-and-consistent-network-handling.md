---
title: Complete and consistent network handling
description: When writing logic that classifies network endpoints (loopback bypass,
  local-vs-remote detection, proxy routing) or applies timeout/cancellation policy,
  make sure the coverage is exhaustive and every code path that performs the actual
  I/O enforces it consistently — not just the primary/happy path.
repository: cline/cline#"><b>zze3729958
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 71067
---

When writing logic that classifies network endpoints (loopback bypass, local-vs-remote detection, proxy routing) or applies timeout/cancellation policy, make sure the coverage is exhaustive and every code path that performs the actual I/O enforces it consistently — not just the primary/happy path.

- Address classification must handle all equivalent representations, not just the obvious case: loopback (`127.0.0.1`, `::1`), `0.0.0.0`, IPv4-mapped IPv6 (`::ffff:127.0.0.1`), and RFC1918/link-local ranges. A check that only matches `127.0.0.0/8` and `::1` will silently misclassify a server bound to `0.0.0.0` (a very common default for local model servers) and send it through the wrong agent/timeout path.
- When a request path has a fallback (e.g. a secondary fetch used when the primary endpoint fails), the fallback must get the same timeout/abort/cancellation treatment as the primary call. An unbounded fallback fetch defeats the purpose of bounding the primary one and can hang the whole operation (e.g. task start) when a host drops packets instead of refusing the connection.
- Don't let library defaults silently override intended behavior: if a proxy-agent or dispatcher applies to all traffic unless explicitly excluded (e.g. `EnvHttpProxyAgent` proxying loopback when `NO_PROXY` isn't set), add the explicit bypass yourself rather than relying on the library's default, and cover it with a regression test using realistic environment variables.
- Treat network timeouts as ambiguous, not as proof of failure: before tearing down a connection or retrying a request, verify the live state (e.g. a bounded health probe, or re-reading server state) rather than assuming failure and resending a write — since the original request may have already succeeded on the server.

Example — exhaustive local-network check:
```ts
const LOCAL_NETWORK_ADDRESSES = new BlockList();
LOCAL_NETWORK_ADDRESSES.addSubnet("127.0.0.0", 8, "ipv4");
LOCAL_NETWORK_ADDRESSES.addAddress("0.0.0.0", "ipv4"); // common "bind all interfaces" default
LOCAL_NETWORK_ADDRESSES.addAddress("::1", "ipv6");
// BlockList.check() also matches IPv4-mapped IPv6 (::ffff:127.0.0.1) against the ipv4 rules.
```

Add regression tests that exercise these edge cases (e.g. `HTTP_PROXY` set with `NO_PROXY` unset, `0.0.0.0` base URLs, a stalled fallback request) rather than only the common-case inputs.