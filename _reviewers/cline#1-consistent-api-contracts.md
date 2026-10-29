---
title: Consistent API contracts
description: 'Keep request/response and wire-protocol contracts honest and symmetric.
  Two concrete rules:


  1. Any field accepted on input must be carried through every corresponding output
  path. If a protocol accepts a new field (e.g. `displayPrompt` on a session input),
  every place that re-emits or projects that event (server projections, host event
  handlers, client...'
repository: cline/cline#1
label: API
language: TypeScript
comments_count: 5
repository_stars: 71024
---

Keep request/response and wire-protocol contracts honest and symmetric. Two concrete rules:

1. Any field accepted on input must be carried through every corresponding output path. If a protocol accepts a new field (e.g. `displayPrompt` on a session input), every place that re-emits or projects that event (server projections, host event handlers, client remaps) must forward it too. A field that goes in and never comes out is a trap for the next integrator — add a regression test that round-trips the field through all projection points.

2. Header, field, and parameter names must truthfully describe the value they carry, and that meaning must not silently change. If `X-Task-ID` is repurposed to carry a `ulid` instead of the task id, either rename the header/field to match its new content or send both values under distinct names — don't let the same identifier mean something different to consumers without warning. Treat this as a breaking change to coordinate with the receiving side (backend, downstream client, etc.).

When your API wraps multiple third-party providers with inconsistent conventions (model list endpoints, context-window field names, versioned paths, region/model-id prefixes), build an explicit normalization layer that enumerates the known variants per vendor (e.g. `context_length` vs `max_model_len`, `/api/v0/models` vs `/api/v1/models`, region-specific inference-profile prefixes) rather than relying on a single hard-coded shape, and add a test case per variant so a new vendor quirk fails loudly instead of silently falling back to a default.

Example of the trap to avoid:
```ts
// Input accepts displayPrompt...
hub.send({ sessionId, prompt, displayPrompt })

// ...but the event projector/back-conversion drops it:
return { sessionId: input.sessionId, input: input.prompt } // displayPrompt lost
```
Forward every accepted field through every output/event path, and verify with a round-trip test.