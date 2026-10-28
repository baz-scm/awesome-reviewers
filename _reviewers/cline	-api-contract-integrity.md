---
title: API contract integrity
description: 'When extending a client-server API or RPC protocol, treat the contract
  as a whole, not a set of independent edits. Concretely:


  1. Register new operations everywhere they must be reachable. A handler that exists
  in code but is missing from an operations allow-list (e.g. `CLOUD_HUB_OPERATIONS`)
  is unreachable through the real transport even though it...'
repository: "cline/cline\t"
label: API
language: TypeScript
comments_count: 7
repository_stars: 70947
---

When extending a client-server API or RPC protocol, treat the contract as a whole, not a set of independent edits. Concretely:

1. Register new operations everywhere they must be reachable. A handler that exists in code but is missing from an operations allow-list (e.g. `CLOUD_HUB_OPERATIONS`) is unreachable through the real transport even though it compiles and looks wired up. Verify end-to-end (ideally with an integration/socket test) that new operations are callable through the actual client, not just unit-tested in isolation.

2. Forward new fields symmetrically. If a new field (e.g. `displayPrompt`) is accepted on the request/input side, it must also be propagated through every corresponding response/event projection that echoes related data back out. A field that goes in but never comes back out is a trap for the next integrator who assumes round-trip support exists.

3. Don't expose client methods the underlying protocol can't actually perform. If there is no server-side command to support an operation (e.g. changing a running session's model), remove or avoid adding the client-facing method rather than leaving a call that always fails.

4. Keep field/header names honest about their content. Don't silently repurpose an existing field or header (e.g. `X-Task-ID`) to carry different data; consumers (including backend services) may depend on its documented meaning. Rename or add a new field instead of changing semantics under an unchanged name.

5. Avoid duplicating contract state. Don't add a second, host-specific flag that mirrors information already available from the canonical shared contract (e.g. a `providerConfigured` boolean duplicating catalog metadata). Derive such flags from the single source of truth (e.g. `apiKeyOptional` on shared provider metadata) so all clients stay in sync automatically instead of needing manual propagation.

Apply these checks whenever adding, renaming, or extending fields/operations in a shared protocol, and add regression coverage that exercises the full round trip (request → server → response/event) rather than just one side.