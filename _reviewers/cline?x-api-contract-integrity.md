---
title: API contract integrity
description: 'Keep request/response and client-interface contracts honest and symmetric
  so integrators are never surprised:


  1. Name fields/headers after what they actually carry. If the content of a field
  changes (e.g. switching a header from sending a task ID to a ulid), rename it instead
  of silently changing the semantics of an existing name — ambiguous names break...'
repository: cline/cline?x
label: API
language: TypeScript
comments_count: 5
repository_stars: 70983
---

Keep request/response and client-interface contracts honest and symmetric so integrators are never surprised:

1. Name fields/headers after what they actually carry. If the content of a field changes (e.g. switching a header from sending a task ID to a ulid), rename it instead of silently changing the semantics of an existing name — ambiguous names break downstream attribution, rate limiting, or joins.
   ```ts
   // Bad: header name no longer matches its content
   "X-Task-ID": this.options.ulid || ""
   // Good: name matches content, or send both explicitly
   "X-Task-ULID": this.options.ulid || ""
   ```
2. Round-trip accepted input through to corresponding output. If an API accepts a new field on a request/event, make sure every place that re-emits or echoes that event also forwards the field. A value that goes in and never comes back out is a trap for the next consumer.
3. Model extensible/optional state with string (or discriminated) unions instead of booleans. Booleans don't scale once a third state appears, and they make invalid combinations representable; prefer `type Mode = "agent_start" | "agent_resume"` over a bare `resumed?: boolean`.
4. Don't add option flags whose only effect duplicates behavior the spec already requires unconditionally — collapse redundant switches into the single real gate (e.g. drop a `mcpApps` flag when tool visibility must be filtered regardless of whether apps are advertised).
5. Keep client interfaces truthful to what the underlying protocol actually supports. If an operation isn't backed by the wire protocol, remove it from the interface (or make it explicitly throw) rather than leaving a method that silently no-ops or lies about capability.

Applying these checks during review — especially for new fields, headers, or client methods — prevents contract drift and keeps the API self-describing for future integrators.