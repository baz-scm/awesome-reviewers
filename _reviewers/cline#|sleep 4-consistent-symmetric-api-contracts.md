---
title: Consistent, symmetric API contracts
description: 'When shaping request/response or event payloads, treat the contract
  as a whole rather than patching one side of it:


  - Round-trip every field. If a field is accepted on input (e.g. `displayPrompt`
  on a submit request), make sure every projection/translation path that turns that
  input into an output event also forwards it. A field that goes in but never...'
repository: cline/cline#|sleep 4
label: API
language: TypeScript
comments_count: 6
repository_stars: 70979
---

When shaping request/response or event payloads, treat the contract as a whole rather than patching one side of it:

- Round-trip every field. If a field is accepted on input (e.g. `displayPrompt` on a submit request), make sure every projection/translation path that turns that input into an output event also forwards it. A field that goes in but never comes out is a trap for the next integrator — grep all copies of the event/record shape, not just the one you touched.
- Don't repurpose an existing field or header's meaning without renaming it. Swapping what a value represents (e.g. sending a `ulid` under a header still called `X-Task-ID`) silently breaks the contract for every consumer that relies on the name to infer the content; either keep the original semantics or introduce a new, clearly-named field/header.
- Avoid duplicating data that already has a canonical source. If a capability or state (e.g. "is this provider configured") is derivable from a shared/catalog contract, expose it there and have consumers read it from that single source, rather than adding a parallel flag to a narrower schema that now needs to be kept in sync.
- Don't offer options or capabilities the underlying implementation can't actually fulfill (e.g. an API method the transport protocol has no command for). If the backend can't support an operation, omit it from the interface rather than exposing a method that always fails or is silently unsupported.
- When a request carries several independent updates (e.g. `prompt`, `title`, `metadata`), forward each as its own field rather than merging them into one generic bag where an explicit value and an implicit default become indistinguishable; otherwise valid update intents (like clearing a title) can be silently dropped downstream.
- Prefer collapsing redundant toggles: if new behavior is really a stricter instance of an existing capability flag's semantics (e.g. filtering tools not meant for the model should always apply once the feature exists, not only when a second flag is also set), fold it into the single switch instead of adding "both must be set" caveats to the docs.

Before merging an API change, check both directions of the data flow (input → every consumer, and every producer → output) and confirm field names, nullability, and defaults stay truthful to what the backend can and will do.