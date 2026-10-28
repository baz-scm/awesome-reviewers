---
title: API contract integrity
description: 'Design request/response payloads, headers, and event fields as a single
  source of truth that accurately and completely describes what they carry:


  1. **Round-trip symmetry**: if an input field is accepted (e.g. `displayPrompt`
  on a prompt-submission request), the corresponding output/event must carry it back
  out. A field that goes in but never comes out is...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: API
language: TypeScript
comments_count: 5
repository_stars: 70973
---

Design request/response payloads, headers, and event fields as a single source of truth that accurately and completely describes what they carry:

1. **Round-trip symmetry**: if an input field is accepted (e.g. `displayPrompt` on a prompt-submission request), the corresponding output/event must carry it back out. A field that goes in but never comes out is a trap for the next integrator — forward it in every projection/handler that mirrors the input.

2. **Names must match semantics**: a header or field name is part of the contract consumers rely on. If the value it carries changes meaning (e.g. `X-Task-ID` starts sending a ulid instead of a task id), either keep the original semantics or rename the field so the name still describes the content. Never silently repurpose a field.

3. **One owner per piece of state**: don't add a new flag/field that duplicates data already derivable from an existing shared contract (e.g. a `providerConfigured` boolean duplicating `Provider.configured`). Surface the fact once, in the canonical shared model, and have all consumers read from it — this avoids synchronization bugs and reduces the surface that must be kept in sync.

4. **Model real states, not loose booleans**: when a field in a request/response/options object can take more than a strict yes/no meaning, prefer a descriptive string enum (e.g. `"seeded" | "written"`) over a boolean. This documents the actual domain states — including what "false" really means — instead of relying on negation.

5. **Trim redundant switches before publishing**: when a capability already has a canonical gate (e.g. a client factory flag that signals a protocol capability), don't add a second option that must be kept in sync with it. Collapse to one switch, especially before the interface ships in a public package — it's far cheaper to simplify pre-release than after the shape is locked in.

Example — mirroring an accepted field back on the matching event, and preferring enums over booleans:
```ts
// Bad: displayPrompt accepted on input is dropped on the way back out
projector.emit("pending_prompt_submitted", { sessionId, input: prompt });

// Good: anything accepted on the request is carried through every projection
projector.emit("pending_prompt_submitted", { sessionId, input: prompt, displayPrompt });

// Bad: ambiguous boolean hides the actual states
interface AgentRunLifecycleContext {
  promptSeeded?: boolean;
}

// Good: enum names the real domain states positively
interface AgentRunLifecycleContext {
  promptOrigin?: "seeded" | "written";
}
```