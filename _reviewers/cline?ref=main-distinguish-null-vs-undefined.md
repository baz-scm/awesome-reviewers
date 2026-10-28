---
title: Distinguish null vs undefined
description: 'When a value can be absent in more than one way—`null`, `undefined`,
  an empty collection, or an omitted field—treat each state as semantically distinct
  and model/check for it explicitly, rather than relying on loose equivalence (`??`,
  `!==`, default parameters) that can silently conflate them. Several bugs in this
  codebase came from exactly this conflation:'
repository: cline/cline?ref=main
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70980
---

When a value can be absent in more than one way—`null`, `undefined`, an empty collection, or an omitted field—treat each state as semantically distinct and model/check for it explicitly, rather than relying on loose equivalence (`??`, `!==`, default parameters) that can silently conflate them. Several bugs in this codebase came from exactly this conflation:

- A loop compared `nextCursor !== undefined` to decide whether to keep paginating, but a server could send `nextCursor: null`, which is not `undefined` and kept the loop spinning. Narrow and validate the actual type instead of comparing against one specific "empty" value:
```ts
cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
```
- A function signature declared `| undefined` while the implementation actually relied on `null` to bypass a parameter default (an explicit `undefined` argument is replaced by the default, so `null` was required to signal "no value here"). Keep the type signature truthful to the runtime contract.
- `metadata: null` was meant to mean "clear the field," but a decoder treated `null` the same as "omitted," turning an intentional clear into a no-op. When null and undefined (or omission) carry different meanings across a serialization/wire boundary, preserve that distinction end-to-end and add a test for it.
- `images ?? retry.images` was meant to fall back to prior attachments when none were supplied, but the transport decoded "no images" as `[]`, not `null`/`undefined`, so `??` never triggered. When "absent" can show up as an empty value rather than `null`/`undefined`, check for that explicitly: `images?.length ? images : retry.images`.
- Conversely, `null` can also be used deliberately as a meaningful sentinel (e.g., "value is still loading") distinct from a default; consumers should check for it explicitly and this state should be covered by tests.

When introducing or reviewing nullable/optional fields: identify every way "no value" can be represented in that context (null, undefined, omitted key, empty string/array), confirm the type declares exactly those cases, and add a regression test for any boundary where one form of "empty" is converted to or compared against another.