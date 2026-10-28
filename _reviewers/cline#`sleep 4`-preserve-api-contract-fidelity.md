---
title: Preserve API contract fidelity
description: 'Treat every field, header, and option on a client-facing interface as
  a contract: its name must always describe what it actually carries, and anything
  accepted on one side of a request/response or input/output pair must be fully honored
  on the other side and across all supported variants.'
repository: cline/cline#`sleep 4`
label: API
language: TypeScript
comments_count: 6
repository_stars: 70979
---

Treat every field, header, and option on a client-facing interface as a contract: its name must always describe what it actually carries, and anything accepted on one side of a request/response or input/output pair must be fully honored on the other side and across all supported variants.

Apply this by:
- Never silently repurpose an existing identifier. If `X-Task-ID` starts carrying a ulid instead of a task id, either keep sending the original value or rename the header (e.g. `X-Task-ULID`) so downstream consumers aren't silently broken.
- When you add a new field to one direction of an API (e.g. `displayPrompt` on request input), make sure every place that projects or converts the paired event/response also forwards it. A field that goes in and never comes back out is a trap for the next integrator — audit all serialization/deserialization paths, not just the one you're touching.
- When consuming third-party or multi-vendor APIs (model-list endpoints, LM Studio/vLLM, etc.), normalize for known naming/versioning variance (`api/v0` vs `api/v1`, `context_length` vs `max_model_len`) instead of hard-coding one vendor's shape and silently falling back to defaults for the rest.
- Favor explicit, self-describing shapes for interface options over booleans or bare strings used as keys (e.g. a getter/setter pair or a string union instead of `"statusWriteQueue"` or a raw `resumed: boolean`). Ambiguous flags are themselves a contract that's easy to violate undetected by the compiler.

Example — keep the contract explicit instead of overloading an existing field:
```ts
// Bad: header name no longer matches what it sends
headers["X-Task-ID"] = options.ulid ?? "";

// Good: rename, or add a second header, so the contract stays unambiguous
headers["X-Task-ULID"] = options.ulid ?? "";
headers["X-Task-ID"] = options.taskId ?? "";
```