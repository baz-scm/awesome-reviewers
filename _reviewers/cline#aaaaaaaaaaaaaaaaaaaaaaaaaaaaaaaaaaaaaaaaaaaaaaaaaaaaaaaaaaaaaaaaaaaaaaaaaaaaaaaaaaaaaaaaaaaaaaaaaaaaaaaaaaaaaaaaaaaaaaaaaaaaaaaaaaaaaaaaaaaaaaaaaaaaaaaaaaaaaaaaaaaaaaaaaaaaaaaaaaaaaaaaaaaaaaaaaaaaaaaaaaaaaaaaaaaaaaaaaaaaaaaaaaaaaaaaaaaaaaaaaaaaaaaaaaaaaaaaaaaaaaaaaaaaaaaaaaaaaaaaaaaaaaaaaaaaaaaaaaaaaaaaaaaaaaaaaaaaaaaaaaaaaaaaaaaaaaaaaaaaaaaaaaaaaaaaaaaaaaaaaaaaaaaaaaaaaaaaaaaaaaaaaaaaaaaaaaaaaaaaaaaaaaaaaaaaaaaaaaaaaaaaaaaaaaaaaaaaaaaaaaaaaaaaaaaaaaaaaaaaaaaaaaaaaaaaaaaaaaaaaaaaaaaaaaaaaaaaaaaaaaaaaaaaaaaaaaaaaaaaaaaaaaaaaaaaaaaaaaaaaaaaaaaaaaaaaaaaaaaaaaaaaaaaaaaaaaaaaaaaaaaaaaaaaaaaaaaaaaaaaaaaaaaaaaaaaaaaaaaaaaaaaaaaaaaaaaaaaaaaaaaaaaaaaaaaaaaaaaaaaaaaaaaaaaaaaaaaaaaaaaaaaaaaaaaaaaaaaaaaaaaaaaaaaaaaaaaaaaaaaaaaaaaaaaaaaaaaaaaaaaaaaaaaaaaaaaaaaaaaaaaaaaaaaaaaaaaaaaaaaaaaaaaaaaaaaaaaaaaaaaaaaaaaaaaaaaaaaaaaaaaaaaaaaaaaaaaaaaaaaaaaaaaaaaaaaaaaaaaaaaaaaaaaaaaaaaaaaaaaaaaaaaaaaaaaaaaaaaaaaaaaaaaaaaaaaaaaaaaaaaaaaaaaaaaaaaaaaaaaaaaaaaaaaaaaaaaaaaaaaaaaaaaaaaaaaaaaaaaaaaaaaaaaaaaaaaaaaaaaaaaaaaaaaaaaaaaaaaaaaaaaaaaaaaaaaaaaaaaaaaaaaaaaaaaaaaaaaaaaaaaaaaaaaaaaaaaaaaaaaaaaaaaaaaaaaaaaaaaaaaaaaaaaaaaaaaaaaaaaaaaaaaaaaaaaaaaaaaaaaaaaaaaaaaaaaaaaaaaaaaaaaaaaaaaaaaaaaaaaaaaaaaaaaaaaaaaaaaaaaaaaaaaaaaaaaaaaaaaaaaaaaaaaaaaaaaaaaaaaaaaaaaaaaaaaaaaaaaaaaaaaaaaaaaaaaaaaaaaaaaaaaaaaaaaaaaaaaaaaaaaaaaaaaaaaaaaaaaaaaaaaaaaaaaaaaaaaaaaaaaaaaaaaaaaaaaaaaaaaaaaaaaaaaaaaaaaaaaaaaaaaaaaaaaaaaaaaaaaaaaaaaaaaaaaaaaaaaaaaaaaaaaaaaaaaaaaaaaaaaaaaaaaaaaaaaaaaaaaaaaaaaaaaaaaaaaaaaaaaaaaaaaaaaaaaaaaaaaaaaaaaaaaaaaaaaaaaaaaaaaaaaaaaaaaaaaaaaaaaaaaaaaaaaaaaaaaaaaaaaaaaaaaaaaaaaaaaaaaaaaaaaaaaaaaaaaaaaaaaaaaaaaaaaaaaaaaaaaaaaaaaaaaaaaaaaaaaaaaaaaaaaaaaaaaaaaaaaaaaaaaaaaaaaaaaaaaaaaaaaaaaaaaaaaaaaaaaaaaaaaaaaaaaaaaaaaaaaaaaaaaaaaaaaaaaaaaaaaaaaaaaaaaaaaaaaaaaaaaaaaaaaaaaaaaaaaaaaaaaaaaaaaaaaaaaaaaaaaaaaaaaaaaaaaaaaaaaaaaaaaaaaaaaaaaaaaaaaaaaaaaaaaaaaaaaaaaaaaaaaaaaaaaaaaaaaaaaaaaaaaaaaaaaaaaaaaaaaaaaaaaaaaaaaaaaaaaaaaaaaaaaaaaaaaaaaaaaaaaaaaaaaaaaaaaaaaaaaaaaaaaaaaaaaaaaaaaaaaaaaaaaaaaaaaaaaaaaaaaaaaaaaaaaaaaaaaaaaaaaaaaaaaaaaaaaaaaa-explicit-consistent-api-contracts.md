---
title: Explicit, consistent API contracts
description: Design interfaces (function signatures, request/response payloads, options
  objects, headers) so their shape unambiguously conveys intent and stays internally
  consistent end-to-end.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: API
language: TypeScript
comments_count: 6
repository_stars: 70976
---

Design interfaces (function signatures, request/response payloads, options objects, headers) so their shape unambiguously conveys intent and stays internally consistent end-to-end.

- Avoid "stringly-typed" or boolean parameters that stand in for a richer concept. A caller passing `"statusWriteQueue"` or a bare `resumed: boolean` gives the compiler nothing to check and the reader nothing to understand; a typo or an invalid combination compiles cleanly. Prefer passing the actual dependency (e.g. a getter/setter pair) or a string-union/discriminated type that only allows valid states:
  ```ts
  // Avoid
  function enqueueWrite<T>(session: Session, queueName: "statusWriteQueue" | "compactionStateWriteQueue", action: () => Promise<T>) {}

  // Prefer
  function enqueueStatusWrite<T>(session: Session, action: () => Promise<T>) {
      return chainWrite(() => session.statusWriteQueue, (q) => (session.statusWriteQueue = q), action);
  }
  ```
- Any field accepted on a request/input must be honored symmetrically on the corresponding response/event — a value that goes in and never comes back out is a trap for the next integrator. When adding a field like `displayPrompt` to an input, forward it through every projection/handler that reconstructs the matching output event, and add a regression test asserting round-trip parity (including empty/omitted cases).
- Don't duplicate authoritative state across multiple contracts or layers (e.g. a desktop-only `providerConfigured` flag mirroring catalog readiness). Surface the single shared source of truth (e.g. `GatewayProviderMetadata.apiKeyOptional` → `ProviderAuthInfo.apiKeyOptional`) and have consumers read from it directly, rather than introducing a second flag that must be kept in sync.
- Keep names accurate to what they carry. If the meaning or type of a value sent across a boundary changes (e.g. a header previously carrying `taskId` now carries `ulid`), either keep the original semantics, rename the field/header to match its new content, or send both values explicitly — never let a name silently diverge from its payload.
- Before an option or flag ships in a public/published surface, simplify it: if a conditional branch (e.g. an `options.mcpApps` toggle) can be replaced by always doing the correct/safe thing, remove the extra switch rather than carrying a caveat about "these two settings must be used together."

Applying this discipline early — especially before an API is published — keeps client code type-safe, prevents silent contract drift, and avoids maintenance debt from duplicated or ambiguous state.