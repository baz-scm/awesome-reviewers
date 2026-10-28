---
title: Consistent, minimal API contracts
description: 'Design request/response and option interfaces so every field is accurate,
  symmetric, and has a single source of truth.


  - Round-trip fields: if a field is accepted on a request, make sure every corresponding
  response/event path also returns it. A field that only goes in and never comes back
  out is a trap for the next integrator (e.g. a `displayPrompt`...'
repository: cline/cline;
label: API
language: TypeScript
comments_count: 6
repository_stars: 70964
---

Design request/response and option interfaces so every field is accurate, symmetric, and has a single source of truth.

- Round-trip fields: if a field is accepted on a request, make sure every corresponding response/event path also returns it. A field that only goes in and never comes back out is a trap for the next integrator (e.g. a `displayPrompt` accepted on input but dropped from the `pending_prompt_submitted` projections until explicitly wired through both copies).
- Name fields/headers for what they actually carry. Changing the value sent under a header or field (e.g. switching `X-Task-ID` from a task id to a ulid) silently breaks the contract for any consumer relying on the name; either keep the original semantics or rename the field so the name and content stay aligned.
- Don't let two parts of the surface duplicate the same fact. If readiness/config state already exists in a shared contract (e.g. `ProviderAuthInfo.apiKeyOptional` from the provider catalog), don't add a parallel flag (`providerConfigured`) on another schema that now needs to be kept in sync — read from the shared source instead.
- Prefer the simplest, least-conditional option set. If a feature flag always implies another check (e.g. MCP visibility filtering should apply regardless of an unrelated `mcpApps` toggle), collapse the redundant option rather than exposing two switches that must be set together.
- Avoid booleans for anything that isn't strictly binary and permanently will stay that way; use a string union when more states exist or may be added, so invalid combinations can't be represented and the API stays easy to test and extend (e.g. prefer `resumeKind: "start" | "resume"` over a boolean plus a separate fallback flag).

Before merging an API or interface change, check: does every accepted field have a corresponding way to read it back out, does every field/header name match its content, is there exactly one owner for each piece of configuration state, and is the option shape the smallest one that still models all valid states?