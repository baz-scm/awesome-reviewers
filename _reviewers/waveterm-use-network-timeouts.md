---
title: Use network timeouts
description: 'Ensure all network operations are cancellable, timeout-protected, and
  executed where the resource lives.


  Motivation

  - Network calls can hang, run on the wrong machine, or transfer too much data. Apply
  consistent patterns to avoid resource leaks, unresponsive reads, and incorrect behavior
  when operating on remote resources.'
repository: wavetermdev/waveterm
label: Networking
language: Go
comments_count: 6
repository_stars: 17328
---

Ensure all network operations are cancellable, timeout-protected, and executed where the resource lives.

Motivation
- Network calls can hang, run on the wrong machine, or transfer too much data. Apply consistent patterns to avoid resource leaks, unresponsive reads, and incorrect behavior when operating on remote resources.

Rules
1) Always use context and timeouts for outbound network calls and dials. Use context-aware APIs (DialContext, http.NewRequestWithContext) and set sensible connect/read timeouts.
   Example (HTTP):
   ctx, cancel := context.WithTimeout(parentCtx, 10*time.Second)
   defer cancel()
   req, _ := http.NewRequestWithContext(ctx, "POST", url, body)
   resp, err := http.DefaultClient.Do(req)

   Example (websocket dial):
   d := websocket.Dialer{HandshakeTimeout: 20 * time.Second}
   conn, _, err := d.DialContext(ctx, wsURL, nil)

2) Make long-running reads cancellable by closing the underlying connection from another goroutine when the context expires. Closing the socket unblocks ReadMessage/Read calls so goroutines don’t leak.
   Example:
   go func() {
       <-ctx.Done()
       conn.Close()
   }()

3) Prefer incremental transfers for streaming channels: send only new/changed messages instead of replaying entire history to reduce bandwidth and contention on shared websockets. If a timeout happens, send a clear partial/final packet (e.g., a timeout or summary packet) so the client retains what it already received.

4) Execute resource-heavy or resource-local operations on the side that owns the resource (server-side) when invoked remotely. For example, create zip archives of a server’s config on the server and then copy the resulting artifact to the client (via filestore/WFS or an explicit transfer), rather than trying to reconstruct the server’s environment on the client.

5) Preserve transport/URI semantics when parsing and serializing (e.g., trailing slashes) so network requests behave as expected.

When to revisit
- If a read goroutine still blocks despite closing the connection, re-check use of non-cancellable APIs; prefer context-aware libraries. Tune timeout values based on operation type (short for quick checks like release queries, longer for large uploads/streams).

References: discussions 0,1,2,3,4,5