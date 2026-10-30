---
title: Null vs undefined semantics
description: When `null`, `undefined`, and "absent/empty" carry different meanings
  (e.g. "explicitly clear this field" vs "not provided, use default" vs "empty value"),
  the code must preserve that distinction end-to-end rather than collapsing them with
  loose equality, `??`, default parameters, or ad-hoc JSON encoding. This matters
  most at serialization/transport...
repository: cline/cline#zzz-unlikely-123abc
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 71035
---

When `null`, `undefined`, and "absent/empty" carry different meanings (e.g. "explicitly clear this field" vs "not provided, use default" vs "empty value"), the code must preserve that distinction end-to-end rather than collapsing them with loose equality, `??`, default parameters, or ad-hoc JSON encoding. This matters most at serialization/transport boundaries (protobuf, JSON-RPC, hub/daemon protocols) and when consuming untrusted external data (MCP servers, model tool calls).

Concrete pitfalls seen in review:
- Using `??` to fall back on a value assumes the "empty" case is `null`/`undefined`, but a serialized default (e.g. protobuf decoding an omitted `images` field as `[]`) silently defeats the fallback. Prefer an explicit check like `images?.length ? images : retry.images` when the "empty" sentinel isn't `null`/`undefined`.
- A field meant to signal "explicitly clear this" (e.g. `baseUrl: null`, `metadata: null`) must not be encoded the same way as "omitted" (e.g. `{}`), or the backend will silently no-op instead of clearing the value.
- A default parameter swallows an explicit `undefined`; if a function needs to distinguish "caller passed nothing" from "caller passed null to mean none," the parameter type and call sites must use `null` deliberately, and the signature must say so.
- Raw/untrusted JSON (e.g. `nextCursor`) should be narrowed to the exact expected type at the boundary (`typeof x === "string" ? x : undefined`) instead of trusting `!== undefined`, since a server-sent `null` is a different value with different control-flow consequences (e.g. an infinite pagination loop).
- When normalizing optional-but-nullable inputs (e.g. a model sending `null` for an unused field), document and implement that `null` is treated as equivalent to omission, rather than letting it leak through.
- Treat an empty collection and a genuinely absent/`null` value as equivalent only when that is the actual intended semantics (e.g. an empty archived-messages array meaning "nothing was saved," same as `null`); otherwise keep them distinct.

```ts
// Bad: relies on `??`, assumes "no attachments" is represented by undefined/null
const images = retry.images ?? images // breaks if images is `[]` from decoding

// Good: makes the "absent" sentinel for this boundary explicit
const images = images?.length ? images : retry.images
```

Before introducing a nullable/optional field or changing how a value is encoded or decoded, be explicit about every state it can be in (not-provided vs explicitly-null vs empty) and verify each boundary (serialization, defaults, `??`, external data parsing) preserves the intended meaning. Add regression tests for the null/empty/absent cases specifically, since they are the ones most often conflated by generic fallbacks.