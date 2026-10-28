---
title: Unambiguous API contracts
description: 'Design interfaces, method signatures, and wire formats so their meaning
  is unambiguous and their behavior matches what callers can rely on:


  - Prefer named options objects over positional boolean parameters, since `load(true,
  true)` is unreadable at the call site and easy to mix up with no type error. Use
  `load({ refresh: true, userInitiated: true })` with...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: API
language: TypeScript
comments_count: 6
repository_stars: 70984
---

Design interfaces, method signatures, and wire formats so their meaning is unambiguous and their behavior matches what callers can rely on:

- Prefer named options objects over positional boolean parameters, since `load(true, true)` is unreadable at the call site and easy to mix up with no type error. Use `load({ refresh: true, userInitiated: true })` with destructured defaults instead.
- Don't add a config flag or field that merely duplicates information already guaranteed elsewhere (a spec rule, another option, or a shared metadata contract). If the spec already mandates filtering tools by `visibility`, don't add a second `mcpApps` toggle that implements the same rule conditionally — collapse it into one source of truth. Likewise, derive readiness/capability flags (e.g. "is this provider configured") from the shared provider contract rather than caching a redundant copy in session config that now needs to stay in sync.
- Keep request/response and event shapes symmetric: any field a client can set on input should be forwarded back out in the corresponding output/event, otherwise it becomes "a trap for the next integrator" who can set it but never read it back.
- Only expose client methods/capabilities that the underlying protocol can actually fulfill; don't add methods like `updateSessionModel` on a host interface if the backend has no corresponding command — remove or guard them so callers can't rely on behavior that silently no-ops.
- Keep identifiers and header/field names honest about their content. If the value a header carries changes semantically (e.g. `X-Task-ID` switching from task ID to ulid), rename the header or send both values explicitly rather than silently repurposing an existing field name — downstream consumers treat the name as the contract.</description>
</invoke>
