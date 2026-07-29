---
title: Preserve API Contracts
description: Maintain deterministic, provider-compatible API contracts by (1) applying
  overrides explicitly and attempt-scoped (no hidden side effects), and (2) preserving
  exact request/response serialization expectations—especially where providers are
  sensitive to JSON schema structure/order or where passthrough/raw modes must not
  be rewritten.
repository: maximhq/bifrost
label: API
language: Go
comments_count: 7
repository_stars: 6862
---

Maintain deterministic, provider-compatible API contracts by (1) applying overrides explicitly and attempt-scoped (no hidden side effects), and (2) preserving exact request/response serialization expectations—especially where providers are sensitive to JSON schema structure/order or where passthrough/raw modes must not be rewritten.

How to apply:
- Overrides/routing: clear any previous attempt state before re-applying request-derived overrides; only allow plugins/hooks to inject routing via the supported Update* APIs (not by directly setting reserved context keys).
- Endpoint/route gating: only parse/extract request fields when you’re sure of the endpoint + content-type; skip admin routes, multipart, and other non-target shapes.
- Raw passthrough modes: when a request is passed through “raw body,” don’t rewrite or inline URLs based on typed structs.
- Serialization contracts: for structured outputs, don’t use plain map decoding/re-encoding when key order matters—use an OrderedMap (or equivalent) and normalize through the same ordered representation end-to-end.

Example (attempt-scoped override wiring):
```go
preReq := resultFromHooks() // may contain ProviderOverride
ctx.ClearValue(schemas.BifrostContextKeyProviderOverride)
if preReq != nil && preReq.ProviderOverride != nil {
    ctx.SetValue(schemas.BifrostContextKeyProviderOverride, preReq.ProviderOverride)
}
```

Example (schema contract preserving order):
```go
type ResponsesTextConfigFormatJSONSchema struct {
    Name   *string          `json:"name,omitempty"`
    Schema *OrderedMap     `json:"schema,omitempty"` // preserves JSON key order
}
```