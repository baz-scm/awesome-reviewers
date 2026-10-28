---
title: API contract fidelity
description: 'Treat request/response shapes, headers, and client-facing options as
  a contract that must stay truthful, symmetric, and single-sourced:


  1. **Round-trip fields.** Any field a caller can send into an API should be echoed
  back wherever semantically relevant, so a field that "goes in and never comes out"
  doesn''t trap the next integrator. Example: when...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: API
language: TypeScript
comments_count: 5
repository_stars: 70986
---

Treat request/response shapes, headers, and client-facing options as a contract that must stay truthful, symmetric, and single-sourced:

1. **Round-trip fields.** Any field a caller can send into an API should be echoed back wherever semantically relevant, so a field that "goes in and never comes out" doesn't trap the next integrator. Example: when `displayPrompt` was accepted on session input, both event-projection paths that convert the submission back out (`session-event-projector.ts` and `HubRuntimeHost`) needed to forward it too, not just the first one that happened to use it.

2. **Never silently repurpose a field or header.** If the data a header/field carries changes meaning, rename it or add a separate field instead of reusing the old name — e.g. don't swap a header from carrying `taskId` to carrying `ulid` while still calling it `X-Task-ID`; either keep the original value, rename to `X-Task-ULID`, or send both as distinct headers. Consumers (rate limiting, attribution, joins) depend on the name describing the content.

3. **Only expose API surface the backend actually supports.** Don't add client methods/options that have no corresponding protocol command — e.g. `updateSessionModel` was removed from `CloudSessionHost` once it was confirmed the Hub protocol has no way to change a running session's model. If a capability doesn't exist server-side, the client interface shouldn't imply it does; let callers detect the missing capability instead.

4. **Single-source shared facts; don't duplicate them in parallel schemas.** When a fact (e.g. "is this provider configured", "is this tool visible to the model") already has an authoritative source (a provider catalog, a capability flag), don't add a second flag elsewhere that must be kept in sync — read/derive it from the shared contract instead. This avoids split sources of truth and removes "these two flags must be set together" caveats from docs.

Apply this by reviewing new/changed request-response types and client methods for: (a) symmetry between what's accepted and what's returned, (b) whether a field's existing name still matches its new meaning, (c) whether the method maps to a real backend capability, and (d) whether the data is already available from an existing shared contract before adding a duplicate.