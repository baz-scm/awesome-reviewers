---
title: Hot Path Cost Controls
description: 'In performance-sensitive paths, actively control hidden costs: cap buffering,
  reuse expensive compiled primitives, and avoid full serialization/large allocations.'
repository: looplj/axonhub
label: Performance Optimization
language: Go
comments_count: 3
repository_stars: 4808
---

In performance-sensitive paths, actively control hidden costs: cap buffering, reuse expensive compiled primitives, and avoid full serialization/large allocations.

Apply these rules:
1) Bound buffering/reads in streaming probes
- Any “pre-read”, “lookahead”, or retry window must have a hard maximum so latency/memory can’t grow unbounded.
- Prefer explicit exit conditions (counts/time) and then hand control back to the main handler.

Example pattern (mimicking the approach):
```go
if !preReadUntilContent && len(buffered) >= maxPreReadEvents {
    break // stop buffering; avoid response delay/unbounded growth
}
```

2) Hoist heavy compiled expressions
- Do not compile regexes inside functions that run frequently. Hoist `regexp.MustCompile(...)` to package/module scope and reuse.

3) Replace full serialization with cheap deterministic signatures
- On hot paths, avoid `json.Marshal` of large structs/slices when you only need routing/decision equivalence.
- Compute a field-level hash/signature (e.g., FNV) over only the fields that can affect behavior, and include nested-condition fields if they impact routing.

Example pattern (self-contained):
```go
func associationSignature(a []*MyAssociation) uint64 {
    h := fnv.New64a()
    for _, x := range a {
        // Write only semantically relevant fields
        h.Write([]byte(x.TargetType))
        h.Write([]byte{byte(x.Enabled)})
        for _, c := range x.Conditions {
            h.Write([]byte(c.Key))
            h.Write([]byte(c.Operator))
            h.Write([]byte(c.Value))
        }
    }
    return h.Sum64()
}
```

4) Test what changed semantics
- When you replace logic (bounded buffering, precompiled parsing, signature computation), add/keep regression tests that cover edge cases and nested variations so you don’t accidentally change the meaning while improving performance.