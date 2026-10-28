---
title: Null vs undefined boundaries
description: Treat `null`, `undefined`, and "empty" (e.g. `[]`, `{}`) as distinct
  signals wherever a value crosses a trust or serialization boundary — external API
  responses, protobuf messages, model-generated tool calls, or JSON persisted through
  another layer — and handle each explicitly instead of assuming they're interchangeable
  or relying on loose operators like...
repository: cline/cline#&&sleep 4
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70980
---

Treat `null`, `undefined`, and "empty" (e.g. `[]`, `{}`) as distinct signals wherever a value crosses a trust or serialization boundary — external API responses, protobuf messages, model-generated tool calls, or JSON persisted through another layer — and handle each explicitly instead of assuming they're interchangeable or relying on loose operators like `??` or `!== undefined`.

Concretely:
- When parsing untrusted/external data, narrow to the exact type you expect and explicitly convert anything else to a known value, rather than trusting the shape. For example, a pagination cursor from a server should be validated, not merely checked against `undefined`:
  ```ts
  cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
  ```
  Here a server-sent `null` would otherwise satisfy `null !== undefined` and spin the loop forever.
- Don't use `??` to backfill a value when the "missing" sentinel on the wire isn't actually `null`/`undefined`. Protobuf omits fields as `[]`/`""`/`0`, not `undefined`, so `images ?? retry.images` silently kept an empty array instead of falling back; check emptiness explicitly (`images?.length ? images : retry.images`).
- When a function parameter has a default value, remember that passing `undefined` triggers the default while passing `null` does not — pick the sentinel deliberately and keep the type signature (`T | null`, not `T | undefined`) consistent with the implementation.
- At serialization/persistence boundaries, confirm whether `null` means "clear this field" versus "field omitted," and preserve that distinction end-to-end. Collapsing `null` into `{}` (or vice versa) can silently turn an intended clear into a no-op, or a no-op into a destructive clear.
- Prefer normalizing nullable inputs to one canonical representation (usually `undefined`) as early as possible, and document why, so downstream code only has to handle one "absent" case instead of juggling `null`, `undefined`, and empty collections everywhere.
- Avoid falling through to a default/happy path when an expected value turns out to be missing in an edge case; fail loudly (throw) instead of silently proceeding with a broken invariant.