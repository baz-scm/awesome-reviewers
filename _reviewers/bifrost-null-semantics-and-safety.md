---
title: Null semantics and safety
description: 'Define and enforce null/optional semantics consistently: (1) treat nil/zero/empty/absent
  as distinct states, (2) clear stale state when nil means “remove”, (3) never rely
  on plain `interfaceValue != nil` when the underlying value may be a typed-nil pointer,
  and (4) when using `omitempty`, only set pointer fields when the value is actually
  present.'
repository: maximhq/bifrost
label: Null Handling
language: Go
comments_count: 5
repository_stars: 6862
---

Define and enforce null/optional semantics consistently: (1) treat nil/zero/empty/absent as distinct states, (2) clear stale state when nil means “remove”, (3) never rely on plain `interfaceValue != nil` when the underlying value may be a typed-nil pointer, and (4) when using `omitempty`, only set pointer fields when the value is actually present.

Practical rules:
- **Clear, don’t skip:** if `nil` is documented as “clears”, ensure your code calls `ClearValue(...)` / resets pointers / zeroes receiver fields rather than leaving previous values intact (especially on reused long-lived contexts).
- **Safe nil detection:** if a value is stored as `interface{}` and may be a pointer, use comma-ok type assertions and/or safe extract helpers that reject typed-nil.
  - Bad: `if x != nil { ... }` when `x` is `interface{}` holding a `(*T)(nil)`.
  - Good: `v, ok := x.(*T); if ok && v != nil { ... }` or `SafeExtract...`.
- **omitempty correctness:** only take addresses / assign pointers when the underlying scalar is non-empty (so `omitempty` truly omits).
- **Preserve invariants and avoid redundant nil guards:** encode assumptions as comments and ensure dereferences are guarded by real construction-time invariants.
- **Reset reusable decoders/receivers:** when custom JSON unmarshalling preserves raw bytes, reset the receiver first to prevent stale preserved fields when decoding the same struct instance multiple times.

Example patterns:

**1) Clear context key on nil**
```go
func setCatalogOnContext(ctx *BifrostContext, catalog ModelInfoProvider) {
  if ctx == nil { return }
  if catalog == nil {
    ctx.ClearValue(BifrostContextKeyModelCatalog) // nil means remove
    return
  }
  ctx.SetValue(BifrostContextKeyModelCatalog, catalog)
}
```

**2) Reject typed-nil in interface{}**
```go
// ctx.Value(...) returns interface{}
if ctx != nil {
  if ov, ok := ctx.Value(BifrostContextKeyProviderOverride).(*ProviderOverride); ok && ov != nil {
    if ov.Key != nil { /* bypass key-pool */ }
  }
}
```

**3) omitempty pointer only when non-empty**
```go
// server_label omitempty should omit when unset
var serverLabelPtr *string
if action.ServerLabel != "" {
  serverLabelPtr = &action.ServerLabel
}
aux := struct{ ServerLabel *string `json:"server_label,omitempty"` }{ServerLabel: serverLabelPtr}
```

**4) Reset receiver before custom unmarshal**
```go
func (m *ResponsesMessage) UnmarshalJSON(data []byte) error {
  *m = ResponsesMessage{} // prevent stale preserved fields
  // ... decode; preserve rawToolSearch only for relevant types
  return nil
}
```

Adopting these rules prevents the common failure modes shown above: stale pointers persisting across requests, incorrect nil checks with typed-nil interfaces, JSON fields that accidentally appear despite `omitempty`, and reused-struct decode bugs.