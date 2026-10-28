---
title: Precise API contracts
description: Design request/response fields, parameters, and headers so their name
  and type precisely describe the data they carry, and avoid duplicating state that
  already exists elsewhere in the contract.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: API
language: TypeScript
comments_count: 4
repository_stars: 70965
---

Design request/response fields, parameters, and headers so their name and type precisely describe the data they carry, and avoid duplicating state that already exists elsewhere in the contract.

- Prefer a descriptive string enum over a boolean when the domain has more than a simple yes/no shape, or when the "false" case needs a positive name rather than a negation. E.g. instead of `promptSeeded?: boolean`, model it as `promptOrigin?: "seeded" | "written"` so every state is named explicitly.
- Never accept a raw string (or boolean) parameter whose valid values are only enforced by convention, where a typo compiles fine but breaks behavior at runtime. Replace "stringly-typed" selectors with a typed getter/setter pair, a dedicated method per case, or a proper enum, e.g. instead of `enqueueWrite(session, "compactionStateWriteQueue", action)`, expose `enqueueCompactionStateWrite(session, action)` built on a shared helper that takes explicit getter/setter functions.
- If a field's semantics change (what value a header or parameter actually carries), rename it to match, don't silently repurpose an existing name. Changing `X-Task-ID` to send a `ulid` while keeping the header name `X-Task-ID` breaks the contract for any consumer relying on that name meaning "task id" — rename the header (e.g. `X-Task-ULID`) or send both values under distinct names.
- Don't add a new field to a request/response payload to mirror information the client can already derive from an existing shared contract (e.g. a catalog or metadata object). Extend the canonical contract instead, so all consumers read a single source of truth instead of keeping two copies in sync.

Applying these rules keeps API payloads self-describing, prevents silent contract drift, and removes a whole class of synchronization bugs between producers and consumers of the same data.