---
title: Type-Safe API Contracts
description: 'When defining or changing an API surface (HTTP headers, SDK calls, event
  payloads), make the contract explicit and hard to misuse:


  - **Follow spec gates unconditionally**: if the spec says the host MUST NOT list
  tools whose visibility doesn’t include `"model"`, don’t wrap that behavior behind
  unrelated flags—remove conditional exceptions.'
repository: cline/cline#v7
label: API
language: TypeScript
comments_count: 5
repository_stars: 70865
---

When defining or changing an API surface (HTTP headers, SDK calls, event payloads), make the contract explicit and hard to misuse:

- **Follow spec gates unconditionally**: if the spec says the host MUST NOT list tools whose visibility doesn’t include `"model"`, don’t wrap that behavior behind unrelated flags—remove conditional exceptions.
- **Ensure round-trip field integrity**: any request field you accept in an input event (e.g., `displayPrompt`) must be preserved in the corresponding outbound/projection events. Add tests for **present**, **explicitly empty**, and **omitted** cases.
- **Avoid boolean positional params**: replace `load(refresh: boolean, background: boolean)` with an options object so call sites can’t silently swap meanings.
  ```ts
  load({ refresh: true, background: true })
  // instead of: load(true, true)
  ```
- **Encode “field only exists in certain states” in types**: use discriminated unions or types that statically represent when fields are set (e.g., only for `beforeRun`).
- **Keep names aligned to semantics**: don’t change the meaning of a field without renaming or adding a second field (e.g., `X-Task-ID` should not suddenly carry ULIDs). If semantics change, rename (`X-Task-ULID`) or send both identifiers separately.

Apply this standard to prevent silent contract breaks, dropped fields, and type-unsafe call sites—especially across layers that project/transform data (client ↔ server, hub envelopes, runtime event handlers).