---
title: API contract consistency
description: Treat request/response shapes, headers, and client-facing methods as
  a contract that must stay internally consistent and truthful about what it carries
  — don't let the surface drift from the semantics or capabilities it actually has.
repository: 'cline/cline

  '
label: API
language: TypeScript
comments_count: 5
repository_stars: 70942
---

Treat request/response shapes, headers, and client-facing methods as a contract that must stay internally consistent and truthful about what it carries — don't let the surface drift from the semantics or capabilities it actually has.

Concretely:
- Round-trip fields: if a field can be set on input, it must be readable on the corresponding output/event, even if no current caller needs it yet. A field that goes in and never comes back out is a trap for the next integrator (e.g. `displayPrompt` accepted on session input must be forwarded in both the server's event projection and the host's event conversion, not silently dropped).
- Keep names truthful: if you repurpose a field or header to carry a different value, rename it or add a new one — don't silently change what an existing name means. Changing `X-Task-ID` to carry a ulid instead of a task id breaks any backend logic keyed on the old semantics and goes empty for callers with no ulid; either keep the original value or expose it under a new, accurately-named header.
- Avoid duplicate sources of truth: don't add a parallel flag/field to one API surface (e.g. a chat session schema) when the same fact is already derivable from the canonical shared contract (e.g. the provider catalog). Surface it from the single shared contract instead of synchronizing two copies.
- Don't expose operations the backing system can't fulfill: if the underlying protocol has no way to perform an action (e.g. changing a running session's model over the Hub protocol), remove that method from the client interface rather than letting it silently fail or no-op — callers should see "not supported" at the type/interface level.
- Prefer collapsing redundant options: if a conditional flag (e.g. `mcpApps`) just gates behavior the spec requires unconditionally anyway, drop the flag and make the behavior the default — fewer knobs means fewer ways for the contract to be misused or misunderstood.

When adding or changing a field in an API surface, ask: does this round-trip correctly, does its name match its content, is it the single source of truth, and does the interface only expose what the implementation can actually do?