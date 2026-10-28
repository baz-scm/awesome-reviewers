---
title: Complete, explicit API contracts
description: 'When extending a request/response surface (RPC commands, Hub operations,
  event payloads, session config), treat the contract as a whole rather than patching
  one side. Two failure modes recur:'
repository: cline/cline?ref=main
label: API
language: TypeScript
comments_count: 6
repository_stars: 70980
---

When extending a request/response surface (RPC commands, Hub operations, event payloads, session config), treat the contract as a whole rather than patching one side. Two failure modes recur:

1. **Incomplete wiring.** A new field or operation is added to the input/request side but never registered or forwarded on the output/response side. Example: `prepareHandoffRepository` was called by client code before it was added to `CLOUD_HUB_OPERATIONS`, so it was unreachable through the real RPC client. Similarly, a `displayPrompt` field was accepted on `send`/`update` input but not threaded through `pending_prompt_submitted` events and the Hub projector, so "a field that goes in and never comes out" becomes a trap for the next integrator. Whenever you add a parameter or capability, trace it through every layer (registry/allowlist, service validation, client exposure, and all corresponding event/response copies) and add a test that exercises the full round trip.

2. **Ambiguous or overloaded parameters.** Booleans and generic blobs hide intent and allow invalid states. A string parameter used only to pick which internal queue to write to (`"statusWriteQueue"` vs `"compactionStateWriteQueue"`) gives the compiler no way to catch a typo — prefer passing a getter/setter pair or a dedicated method per case instead of a magic string. Likewise, a `resumed?: boolean` flag models state machines poorly; prefer a string union (or richer explicit field) when there are more than two meaningful states or when the state can be owned differently per caller. The same logic applies to response/update APIs: folding `prompt`/`title` into a generic `metadata` blob loses the ability to distinguish "clear this value" from "leave it unchanged," so dedicated fields should be forwarded explicitly rather than merged into a catch-all object.

```ts
// Avoid: stringly-typed selector, easy to typo, not type-checked
enqueueWrite(session, "compactionStateWriteQueue", action);

// Prefer: dedicated method or explicit getter/setter pair
enqueueCompactionStateWrite(session, action);
```

Before merging any API change, confirm: every accepted field has a path back out where relevant, every new operation is registered wherever operations are allow-listed, and every parameter's type makes invalid combinations unrepresentable rather than relying on documentation or caller discipline.