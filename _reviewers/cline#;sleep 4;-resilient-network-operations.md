---
title: Resilient network operations
description: 'Network code must be defensive against the ways real connections fail:
  slow peers, brief drops, malformed data, and topology edge cases. Concretely:


  - Bound every outbound request. Every `fetch`/socket call, including fallback paths,
  needs an explicit timeout or `AbortSignal` — an "unbounded on error only" fetch
  (e.g. a fallback hit when the primary call...'
repository: cline/cline#;sleep 4;
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70976
---

Network code must be defensive against the ways real connections fail: slow peers, brief drops, malformed data, and topology edge cases. Concretely:

- Bound every outbound request. Every `fetch`/socket call, including fallback paths, needs an explicit timeout or `AbortSignal` — an "unbounded on error only" fetch (e.g. a fallback hit when the primary call times out) can hang a task forever even though the primary path is safe.
- Treat brief disconnects as recoverable, not fatal. Don't fail a read or cancel a pending request the instant a socket drops; wait for reconnection within a bounded grace period and retry once, only failing for real after that window (see hub transcript reads waiting on `HubLink.connected(withinMs)` and the follow-up question of whether open `askQuestion` requests should get the same grace instead of being cancelled immediately on disconnect).
- Never let unparseable or unexpected wire data crash the process. Wrap frame/message parsing in try/catch; on failure, close the connection cleanly with a real error so pending callers get a normal rejection and reconnect logic takes over, rather than throwing inside a socket event listener.
- Get network-address edge cases right and test them explicitly: loopback/local-network detection must cover all spellings (`127.0.0.1`, `0.0.0.0`, IPv4-mapped IPv6 like `::ffff:127.0.0.1`), and proxy-bypass logic must still route loopback directly even when `HTTP_PROXY` is set and `NO_PROXY` is absent. Write regression tests that set these env vars/addresses explicitly rather than only testing the "nothing configured" case.
- When adding retry/fallback/bind-fallback behavior, make the opt-in explicit and let an explicit caller-supplied endpoint or option always win over an inferred default, so deliberate configuration (a fixed port, a fixed proxy) is never silently overridden.

Example of the parse-failure pattern to apply broadly:
```ts
socket.addEventListener("message", (data) => {
  let frame: HubTransportFrame;
  try {
    frame = JSON.parse(decodeSocketData(data)) as HubTransportFrame;
  } catch (error) {
    // Don't throw in a socket listener (kills the process). Close with a
    // real cause instead so pending replies reject and reconnect runs.
    this.closeWithError(new HubTransportError("hub_connection_closed", ...));
    return;
  }
  this.handleFrame(frame);
});
```