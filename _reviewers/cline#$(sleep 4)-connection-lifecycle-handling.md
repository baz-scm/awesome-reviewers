---
title: Connection lifecycle handling
description: 'For stateful, multi-client network services (hubs, session servers,
  RPC brokers), explicitly design and test the behavior for client disconnects, reconnects,
  and ownership hand-off instead of leaving it implicit. In particular:'
repository: cline/cline#$(sleep 4)
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70978
---

For stateful, multi-client network services (hubs, session servers, RPC brokers), explicitly design and test the behavior for client disconnects, reconnects, and ownership hand-off instead of leaving it implicit. In particular:

- Never let a reconnect or re-start request silently replace a live, in-progress session/run; detect that the existing state is still active and reattach to it (or reject the request) rather than orphaning the old state and routing new requests to a stale copy.
- Track which connected clients can service a given capability/callback so that when the original owner disconnects, another still-connected and still-attached client that registered the same capability can transparently take over. Only treat "no eligible client" as a hard failure.
- Distinguish a transient disconnect from an explicit detach/stop: an explicit detach must immediately cancel its pending requests and must not be considered an eligible owner again until it re-attaches, whereas a transient drop may warrant a short grace period before cancelling (but should still cancel immediately on an explicit stop).
- Add targeted tests for each of these edge cases: starting a session that's already running, the original owner disconnecting mid-request, a client detaching while still connected, and a replacement client taking over mid-run.

Example from a hub server: record every client that registers a given capability for a session; route a capability request to the original owner while connected, otherwise to the next connected, attached client that registered it; cancel pending requests to a client immediately once it explicitly detaches, and surface a clear "disconnected — send a message to continue" error only when no eligible client remains.