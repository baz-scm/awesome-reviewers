---
title: API contract consistency
description: 'When extending a request/response contract, treat it as a single, symmetric
  interface rather than a grab-bag of ad-hoc flags. Concretely:


  1. Round-trip new fields: if a field is accepted on input (e.g. `displayPrompt`
  on a pending-prompt request), it must be forwarded through every corresponding output/event
  path (session projector, runtime host, hub...'
repository: cline/cline#$(sleep 4)
label: API
language: TypeScript
comments_count: 7
repository_stars: 70978
---

When extending a request/response contract, treat it as a single, symmetric interface rather than a grab-bag of ad-hoc flags. Concretely:

1. Round-trip new fields: if a field is accepted on input (e.g. `displayPrompt` on a pending-prompt request), it must be forwarded through every corresponding output/event path (session projector, runtime host, hub envelope, etc.). A field that goes in but never comes back out is a trap for the next integrator — add a regression test that exercises the full round trip, including edge cases like an omitted or empty value.

2. Derive capabilities from a single source of truth instead of adding parallel flags. Don't invent a new option (`mcpApps`, `providerConfigured`) to express something the existing contract/spec already encodes (visibility metadata, `apiKeyOptional` on provider metadata). Duplicated flags drift out of sync and add unnecessary surface area — collapse them into the existing contract and gate behavior off that.

3. Keep names and types honest about their semantics. A header or field name is part of the contract consumers rely on; if the value's meaning changes (e.g. `X-Task-ID` now carrying a `ulid` instead of a task id), rename it or add a separate field rather than silently repurposing it.

4. Prefer extensible types over booleans for options that model state. A boolean (`resumed: boolean`) often can't express future states cleanly and tends to proliferate into a tangle of flags with invalid combinations. Use a string union or small enum when more than two meaningful states (now or in the future) are plausible.

Example — round-tripping a new input field:
```ts
// Input: displayPrompt is accepted
hubRuntimeHost.send({ sessionId, prompt, displayPrompt })

// Output: displayPrompt must be forwarded on the way back out
case "pending_prompt_submitted":
  return { ...event, displayPrompt: input.displayPrompt }
```
Apply this checklist whenever adding or modifying API surface: trace every new field across both directions of the contract, check whether an existing shared field already covers the need, and verify names/types still describe what they carry.</description>
