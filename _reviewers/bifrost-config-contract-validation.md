---
title: Config Contract Validation
description: Ensure API configuration endpoints (e.g., `PUT /api/config`) define and
  enforce a precise request/response contract across schema shape, merge semantics,
  validation behavior, and persistence.
repository: maximhq/bifrost
label: API
language: Json
comments_count: 2
repository_stars: 6862
---

Ensure API configuration endpoints (e.g., `PUT /api/config`) define and enforce a precise request/response contract across schema shape, merge semantics, validation behavior, and persistence.

Apply this standard:
- **Schema must match canonical payload serialization.** For complex/credential fields, your JSON Schema should validate the exact shape your server produces/round-trips (e.g., secret references). Validate with the same Draft/validator behavior used in production.
- **Strict validation with no state change on rejection.** If a payload is invalid (unknown enum, incompatible sub-objects, wrong auth-mode config), return **400** and guarantee the config is **not mutated**.
- **Explicit partial-merge vs reset semantics.** If the endpoint performs a partial merge, omitted fields must preserve existing stored values (do not “default reset”). Document this behavior and test it.
- **Test the contract end-to-end.** Add E2E tests that:
  - PUT invalid config ⇒ 400 and assert GET round-trip shows no change.
  - PUT valid config ⇒ GET confirms persistence.
  - When behavior is mode-dependent, assert the correct branch (and that security flips only when intended).

Example (server-side merge rule pattern):
```go
// Only update each field when explicitly provided so partial PUTs do not clear stored values.
if payload.ClientConfig.MCPServerAuthMode != "" {
    updatedConfig.MCPServerAuthMode = payload.ClientConfig.MCPServerAuthMode
}
// otherwise keep currentConfig.MCPServerAuthMode
```

Example (E2E assertion pattern):
- PUT invalid payload ⇒ expect `400` and response text includes the relevant field name.
- Then GET `/api/config` and assert the boot/auth mode equals the preexisting value (round-trip persistence).