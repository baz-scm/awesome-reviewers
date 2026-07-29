---
title: Bounded, Targeted Performance
description: 'When optimizing performance, avoid whole-object work and unbounded resource
  growth. Apply these standards:


  1) Targeted extraction/rewrites (no full parsing)'
repository: maximhq/bifrost
label: Performance Optimization
language: Go
comments_count: 8
repository_stars: 6862
---

When optimizing performance, avoid whole-object work and unbounded resource growth. Apply these standards:

1) Targeted extraction/rewrites (no full parsing)
- If you only need one JSON field, read it with gjson/sonic.Get and rewrite with sjson, rather than unmarshalling the full body/request.
- Guard on JSON shape before using sjson.Set to avoid corrupting non-JSON/multipart bodies.

Example (safe “model” rewrite):
```go
func rewriteTopLevelModel(body []byte, alias, modelID string) []byte {
  trimmed := bytes.TrimLeft(body, " \t\r\n")
  if len(trimmed) == 0 || trimmed[0] != '{' { // multipart/form-data etc.
    return body
  }
  cur := gjson.GetBytes(body, "model")
  if cur.Type != gjson.String || !strings.EqualFold(cur.Str, alias) {
    return body
  }
  out, err := sjson.SetBytes(body, "model", modelID)
  if err != nil { return body }
  return out
}
```

2) Bound buffering and “perpetual due” logic
- Any paused replay buffer, retry loop, or time-based scheduler must have hard limits (e.g., max bytes) and fail-closed handling for invalid/negative durations.

3) Coalesce duplicate concurrent work
- For expensive refresh/exchange operations, use singleflight (or equivalent) so only one goroutine performs the work per key while others wait.

4) Pooling hygiene (prevent allocation retention)
- If you use pooled objects, clear embedded request/state that retains large allocations before returning to the pool (do in-place zeroing; don’t rely on GC).

These practices together reduce CPU spent on unnecessary parsing/scanning, prevent memory blowups, and eliminate wasted concurrent work—directly improving throughput and latency.