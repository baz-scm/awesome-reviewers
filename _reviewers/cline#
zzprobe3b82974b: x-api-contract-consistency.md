---
title: API contract consistency
description: 'Treat every client-facing interface — tool APIs, RPC operations, request/response
  fields, and HTTP headers — as a contract that must stay complete, unambiguous, and
  centrally enforced:'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: API
language: TypeScript
comments_count: 8
repository_stars: 71067
---

Treat every client-facing interface — tool APIs, RPC operations, request/response fields, and HTTP headers — as a contract that must stay complete, unambiguous, and centrally enforced:

- **Wire every operation end-to-end.** If a method is added to a client or host implementation, it must also be registered wherever operations are allow-listed or dispatched (e.g. an RPC's operation registry), otherwise it is unreachable even though it compiles. Verify new capabilities with a round-trip test through the actual client, not just the implementation.
- **Match names to semantics.** A field or header name implies a specific meaning to callers (and to downstream services). If the value it carries changes (e.g. a header moves from sending `taskId` to sending `ulid`), rename the field/header or add a new one — don't silently repurpose it while keeping the old name, and don't let it become empty for cases the old value always covered.
- **Model multi-state concepts as enums, not booleans.** A flag like `promptSeeded?: boolean` hides what "false" actually means. Prefer a descriptive string union (e.g. `entry: "run" | "continue"`, `seeded: "seeded" | "written"`) so every state is named positively and new states can be added without redefining what `false` means.
- **Don't let optional flags encode behavior the contract already requires.** If the underlying spec mandates a behavior unconditionally (e.g. hiding tools not visible to the model), don't gate it behind an extra option — collapse it into the single switch that already exists, especially before the surface ships publicly.
- **Centralize validation instead of duplicating it with diverging rules.** When two layers (e.g. core and a host/sidecar) both reimplement the same precondition checks (remote URL validation, account/session checks) they will drift. Resolve/validate once in the authoritative layer, carry the resulting state (e.g. a scope token or plan) to subsequent calls, and keep only the genuinely layer-specific step (e.g. the final push) outside it.
- **Normalize client-side request construction** (base URLs, path prefixes, versions) consistently with how the runtime already builds the same request, and add tests for the edge cases (trailing slashes, existing version segments, proxy prefixes).

Example of the enum-over-boolean fix:
```ts
// Before
promptSeeded?: boolean;

// After
entry?: "run" | "continue";
promptSource?: "seeded" | "written";
```