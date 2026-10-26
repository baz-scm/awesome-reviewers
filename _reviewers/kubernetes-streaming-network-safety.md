---
title: Streaming network safety
description: 'When adding or modifying network transports/proxies/stream multiplexing
  (HTTP RoundTripper, SPDY↔websocket translators, port-forward websockets), treat
  it as a lifecycle + overload problem:'
repository: kUbernetes/kUbernetes
label: Networking
language: Go
comments_count: 6
repository_stars: 128688
---

When adding or modifying network transports/proxies/stream multiplexing (HTTP RoundTripper, SPDY↔websocket translators, port-forward websockets), treat it as a lifecycle + overload problem:

- **Lifecycle hygiene:** if your networking code short-circuits (returns early), still close/cleanup inputs you own (e.g., `req.Body`).
- **Connection readiness:** handle transient/long-blocking periods explicitly (e.g., prefer `grpc.WaitForReady(true)` for notification delivery instead of assuming an existing connection will still be usable).
- **Multiplexing and buffering:** do not assume websocket multiplexing provides SPDY-style backpressure. Implement **explicit throttling/concurrency limits** and monitor where large requests start causing buffering/blocking; add mitigations before GA (alpha/beta gating as appropriate).
- **Test reality:** when failures depend on protocol details (proxy TLS/dialer behavior, shared ports), build tests that reproduce the real conflict/error so the failure mode is deterministically exercised.

Code sketch (resource + readiness + bounded buffers):
```go
// 1) Resource hygiene in RoundTrip short-circuit.
func (t *FaultInjectingTransport) RoundTrip(req *http.Request) (*http.Response, error) {
    defer func() {
        if req.Body != nil {
            _ = req.Body.Close()
        }
    }()
    // ... inspect req, possibly return synthesizeResponse(...) early ...
}

// 2) Connection readiness for long/fragile RPC paths.
// (pattern: wait for readiness rather than assuming the old connection is still good)
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
client := /* new grpc client over the same dial target */
if err := client.NotifyRegistrationStatus(ctx, payload /*...*/,
    grpc.WaitForReady(true),
); err != nil {
    return err
}

// 3) Gate websocket multiplexing concurrency/buffer growth.
// Enforce per-connection request/stream limits and timeouts.
if activeStreams.Load() > maxAllowed {
    return fmt.Errorf("too many concurrent websocket streams")
}
```

Applying this checklist prevents subtle correctness regressions (wrong protocol state, lost notifications), leaks (unclosed bodies/connections), and production outages when switching from SPDY-like backpressure to websocket multiplexing.