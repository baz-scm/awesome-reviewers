---
title: Bound and validate network paths
description: 'Treat every outbound network call — including fallbacks, retries, and
  reconnects — with the same rigor as the primary path: apply explicit timeouts/AbortSignals
  everywhere a request can block, and never leave a secondary code path unbounded
  just because the happy path is covered. For example, if a primary model-list fetch
  has a 5s abort but its fallback...'
repository: cline/cline?foo=bar
label: Networking
language: TypeScript
comments_count: 8
repository_stars: 71082
---

Treat every outbound network call — including fallbacks, retries, and reconnects — with the same rigor as the primary path: apply explicit timeouts/AbortSignals everywhere a request can block, and never leave a secondary code path unbounded just because the happy path is covered. For example, if a primary model-list fetch has a 5s abort but its fallback uses a bare `fetch`, a host that drops packets instead of refusing will hang the fallback forever and block task startup; the fallback needs the same AbortSignal.

Likewise, keep connection routing and reuse decisions consistent with established conventions instead of introducing silent divergence. A custom dispatcher that disables idle timeouts must still honor existing proxy/loopback rules (e.g. localhost/127.0.0.1 must stay direct even when `HTTP_PROXY` is set and `NO_PROXY` is unset) — overriding one behavior (idle timeout) should not accidentally change another (routing).

When caching or reusing a connection/socket/control-path, key reuse to the actual identity being connected to (endpoint URL, credentials, auth token). Reconnect or rebuild the connection when identity changes, but keep the existing connection when only unrelated metadata changes (e.g. a name-only profile edit should preserve the SSH control master, while a credential change must close it and allocate a fresh one).

Finally, when checking if a remote peer is a valid target for a request, verify real eligibility (e.g., still attached/authorized to the session), not just "socket is open" — a client that explicitly detached or left should be skipped even if its transport connection technically remains, so requests route to a peer that can actually respond.