---
title: Preserve API Contracts
description: When changing or adding API-visible behavior (endpoints, request headers,
  event envelopes, tool/function exposure, URL normalization), ensure the contract’s
  *semantics* remain consistent and the data propagates end-to-end.
repository: cline/cline#v29
label: API
language: TypeScript
comments_count: 6
repository_stars: 70893
---

When changing or adding API-visible behavior (endpoints, request headers, event envelopes, tool/function exposure, URL normalization), ensure the contract’s *semantics* remain consistent and the data propagates end-to-end.

Practical rules:
1) **Don’t change meaning under the same name**: if a header/field name remains the same, its value must keep the same semantic contract. If semantics change, rename the field (or add a new header/field) and update backend/client together.
2) **Follow the spec unconditionally**: for capability/spec rules (e.g., MCP tool `visibility`), apply the rule directly instead of gating behavior on unrelated feature flags. If the host wasn’t advertising a capability, you still must not expose tools the model must not see.
3) **Forward every payload field end-to-end**: if an input/event contains a new field (e.g., `displayPrompt`), add it to *all* projections/copies so it doesn’t disappear between layers.
4) **Centralize and standardize normalization**: URL versioning/path rules (trailing slashes, `/v1` prefixing) should be applied consistently with the runtime’s normalization logic; avoid duplicating “legacy” assumptions.
5) **Make exported interfaces unambiguous**: avoid boolean parameter lists in public functions/callback factories; prefer an options object.

Example pattern (options object):
```ts
// Before (ambiguous at call site)
load(refresh, background)

// After (self-documenting)
load({ refresh: true, background: true })
```

Example pattern (end-to-end field forwarding):
```ts
// When projecting/copying events, preserve the field everywhere
projectPendingSubmitted(input) {
  return {
    ...input,
    displayPrompt: input.displayPrompt, // carry through both copies
  }
}
```