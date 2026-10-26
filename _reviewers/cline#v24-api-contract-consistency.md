---
title: API Contract Consistency
description: 'When code crosses an API boundary (hub/RPC, HTTP, event projection,
  or tool catalog), preserve the contract end-to-end: semantics must not silently
  change, required fields must be forwarded everywhere, and spec-required filtering
  should be unconditional.'
repository: cline/cline#v24
label: API
language: TypeScript
comments_count: 5
repository_stars: 70891
---

When code crosses an API boundary (hub/RPC, HTTP, event projection, or tool catalog), preserve the contract end-to-end: semantics must not silently change, required fields must be forwarded everywhere, and spec-required filtering should be unconditional.

Apply this standard:
- **Field passthrough:** If a request/event includes a property (e.g., `displayPrompt`), ensure every projection/copy path forwards it. Add a regression test that fails if the field is omitted or differs.
- **Header/request semantics:** If you change what a header value represents, either **keep the old meaning** or **rename the header / add a new header** so the backend contract remains unambiguous (don’t repurpose `X-Task-ID` to carry a different identifier).
- **Reachability & version safety:** Ensure required RPC operations are registered/exposed on both sides. If the operation depends on account/scope, carry an explicit scope token through subsequent calls to prevent silent account switching.
- **Spec-driven behavior:** Implement server-side/tool-list behavior to match the spec (e.g., do not list tools whose `visibility` doesn’t include the required target) without tying compliance to unrelated feature flags.
- **Intent clarity in API-like functions:** Avoid ambiguous boolean parameters in request builders; prefer an options object (e.g., `load({ refresh: true, background: true })`).

Example (field passthrough + explicit options):
```ts
// Good: explicit intent via an options object
load({ refresh: true, userInitiated: true });

// Good: passthrough a request field through multiple layers
function toHubEnvelope(coreEvent: CoreSubmittedEvent) {
  return {
    ...coreEvent,
    displayPrompt: coreEvent.displayPrompt, // must be copied in both directions
  };
}
```

This prevents “works today” behavior that breaks attribution, telemetry, tool selection, recovery flows, or downstream integrators later.