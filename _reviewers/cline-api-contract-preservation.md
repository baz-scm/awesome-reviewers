---
title: API Contract Preservation
description: 'Always preserve the meaning of public/API-facing inputs and fields across
  client/server boundaries.


  Apply this checklist:

  - Round-trip fields: if a request/event accepts a new field, ensure every projection/conversion
  path carries it through (avoid “write-only” fields).'
repository: cline/CLINE
label: API
language: TypeScript
comments_count: 6
repository_stars: 70839
---

Always preserve the meaning of public/API-facing inputs and fields across client/server boundaries.

Apply this checklist:
- Round-trip fields: if a request/event accepts a new field, ensure every projection/conversion path carries it through (avoid “write-only” fields).
- Bind scope explicitly: when performing multi-step RPCs, snapshots/tokens should carry the original scope (e.g., account/provider/session) so later calls cannot silently switch context.
- Never change identifier meaning without renaming: if you change what a header/value represents (e.g., task ID → ULID), either keep the original semantic value or rename the header (and document). If both are needed, send both distinctly.
- Enforce spec invariants unconditionally: if the contract says “must not list tools whose visibility excludes model,” do it regardless of optional feature flags.
- Safe URL/version normalization: do not inherit defaults that alter user-supplied semantics (e.g., don’t append/assume a version path for “user-supplied full URLs”). Always normalize trailing slashes/version prefixes consistently.

Example (header semantics):
```ts
// Prefer either stable semantics:
headers["X-Task-ID"] = taskId;

// Or make the contract explicit when semantics changed:
headers["X-Task-ID"] = taskId;
headers["X-Task-ULID"] = ulid;
```

Example (field round-trip):
```ts
// Ensure converters/projectors preserve new fields.
// If hub input includes displayPrompt, emit it in the hub envelope,
// and in HubRuntimeHost’s event conversion.
```