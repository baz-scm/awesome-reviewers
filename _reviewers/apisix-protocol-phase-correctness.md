---
title: Protocol phase correctness
description: When writing networking plugins/adapters, make behavior consistent with
  the request/stream lifecycle and the actual protocol/runtime semantics—then lock
  it with targeted regression tests.
repository: apache/apisix
label: Networking
language: Other
comments_count: 7
repository_stars: 16922
---

When writing networking plugins/adapters, make behavior consistent with the request/stream lifecycle and the actual protocol/runtime semantics—then lock it with targeted regression tests.

Apply these rules:
1) Run auth/identity work in the correct phase for downstream lifecycle
- If other plugin outputs (e.g., Consumer/Consumer Group) must see the result, ensure the network call completes before the core merge point.
- If multiple plugins may attach the same identity, document the ordering/merge model and add a guard if conflicts are possible.

2) Don’t keep outdated or transport-specific protocol guards
- For H2/H3, implement body/read logic based on current runtime behavior (e.g., don’t block valid requests due to legacy Content-Length assumptions).

3) Streaming must be event-correct (one-shot + EOF/terminal events)
- Gate “scan/replace/release” logic so it executes exactly once per response (especially when protocol converters emit multiple terminal events).

Example (one-shot release pattern):
```lua
-- before buffering/replacing chunks
if not ctx.lakera_response_released then
  ctx.lakera_response_released = false
end

-- on any terminal condition that indicates end-of-stream assembly
if ctx.lakera_response_released == false then
  ctx.lakera_response_released = true
  -- scan+release (or deny) exactly once
end
```

4) Avoid hardcoding transport assumptions; make scheme/endpoint configurable
- Don’t hardcode `https://` if deployments/tests may use plain HTTP (or configure an override similar to other managers).

5) Centralize forwarded address/host handling; fix at the root cause
- If the platform already normalizes `X-Forwarded-*`, reuse that canonical form rather than duplicating trust/untrust branching across features.

6) Connection lifecycle: use keepalive pooling and treat abort hooks as singletons
- Prefer `connect -> request -> set_keepalive` to avoid per-call TCP overhead.
- If you use `ngx.on_abort`, document that it’s a single registration per request and ensure this endpoint/plugin lifecycle is dedicated or otherwise guarded.

Always add targeted tests around the networking edge you’re touching: H2/H3 body handling, streaming duplication/drop scenarios (with converters), forwarded-host/redirect behavior, and TLS vs non-TLS transport expectations.