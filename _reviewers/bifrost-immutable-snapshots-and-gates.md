---
title: Immutable Snapshots And Gates
description: When concurrency crosses subsystem boundaries (HTTP handlers, streaming,
  background workers, plugin hooks), treat shared state as immutable and coordinate
  lifecycle explicitly.
repository: maximhq/bifrost
label: Concurrency
language: Go
comments_count: 10
repository_stars: 6862
---

When concurrency crosses subsystem boundaries (HTTP handlers, streaming, background workers, plugin hooks), treat shared state as immutable and coordinate lifecycle explicitly.

**Coding standards**
1) **Snapshot/clone before publishing**
- Never return or store pointers/maps/slices that remain aliases to internal catalog/store data that other goroutines may mutate.
- Prefer immutable snapshots and atomic swaps for hot-reload config (and clone any slice/map contents).

2) **Hold locks only for state access; release before blocking/calling out**
- Lock to take a consistent snapshot, then unlock before invoking callbacks, restarting goroutines, or doing any potentially blocking work.
- Design around lock ordering and avoid re-entrant lock reads.

3) **Make streaming/background lifecycle coordination explicit**
- Use dedicated gate/flusher lifecycle state and ensure cleanup ordering can’t delay client-visible release.
- Always wire cancellation into streaming fan-out and flusher drain paths; ensure paused/end/cleanup transitions are deterministic.

**Example pattern (immutable config swap)**
```go
type CorsMiddleware struct {
  cfg atomic.Pointer[MyConfigSnapshot]
}

type MyConfigSnapshot struct {
  AllowedOrigins []string
  AllowedHeaders []string
}

func NewCorsMiddleware(cfg *MyConfig) *CorsMiddleware {
  m := &CorsMiddleware{}
  snap := &MyConfigSnapshot{
    AllowedOrigins: slices.Clone(cfg.AllowedOrigins),
    AllowedHeaders: slices.Clone(cfg.AllowedHeaders),
  }
  m.cfg.Store(snap)
  return m
}

func (m *CorsMiddleware) UpdateConfig(cfg *MyConfig) {
  snap := &MyConfigSnapshot{
    AllowedOrigins: slices.Clone(cfg.AllowedOrigins),
    AllowedHeaders: slices.Clone(cfg.AllowedHeaders),
  }
  m.cfg.Store(snap)
}
```

**Review checklist**
- Does this code publish (or store) any pointer to shared mutable structures across goroutines/requests?
- Are we cloning maps/slices/attribute maps that might be mutated later?
- Are we holding a mutex while calling out / restarting / doing I/O (risking deadlock or re-entrancy)?
- For streaming, do paused/end/cleanup transitions ensure deterministic flusher behavior and correct client release under cancellation?
- Do we have tests that actually exercise timing-sensitive paths (not only unit-level outcomes)?