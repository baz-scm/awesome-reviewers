---
title: Design stable, semantic contract fields
description: 'Treat every field added to a shared interface (SDK types, request/response
  payloads, hook options, headers) as a long-term API commitment, and design it deliberately:'
repository: cline/cline
label: API
language: TypeScript
comments_count: 6
repository_stars: 70886
---

Treat every field added to a shared interface (SDK types, request/response payloads, hook options, headers) as a long-term API commitment, and design it deliberately:

- Prefer a descriptive string-literal union over a boolean when the field models more than a true/false fact. Booleans often hide states that aren't really the negation of each other, and they tend to proliferate into combinations that are invalid and hard to test. Favor `entry?: "run" | "continue"` over `isContinuation?: boolean`, and `resumed?: "resumed" | "started"` over `resumed?: boolean` — the enum documents the "false" case positively instead of through negation.
- Keep contracts symmetric: if a field can be set on input, make sure every code path that produces the corresponding output also forwards it. A field that goes in but never comes back out (e.g. `displayPrompt` accepted but dropped by an event projector) is a trap for the next integrator even if no current caller depends on it.
- Never silently repurpose an existing field or header's meaning. If `X-Task-ID` used to carry the task id and now needs to carry a ulid, rename it (`X-Task-ULID`) or add a new field/header instead of changing what the existing name means underneath callers.
- Don't duplicate a fact that's already derivable elsewhere in the contract (e.g. a `providerConfigured` flag duplicating a provider catalog's own `configured`/`apiKeyOptional` metadata). Expose the single source of truth and let consumers read from it, avoiding extra synchronization burden.
- Before shipping a new option/flag on a public surface, check whether it can be collapsed into existing, always-on behavior; it's far cheaper to simplify the surface before it's published than after.

Applying these checks during review prevents ambiguous, inconsistent, or redundant contracts from leaking into the public API surface.