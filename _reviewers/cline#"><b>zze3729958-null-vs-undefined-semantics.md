---
title: Null vs undefined semantics
description: 'Several bugs came from treating `null`, `undefined`, and "empty" values
  (`""`, `[]`, `{}`) as interchangeable when they actually carry different meanings:
  "absent/not provided" vs "explicitly cleared" vs "present but empty". Before writing
  a null/undefined guard, confirm exactly which sentinel the data source uses for
  each case, especially across...'
repository: cline/cline#"><b>zze3729958
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 71067
---

Several bugs came from treating `null`, `undefined`, and "empty" values (`""`, `[]`, `{}`) as interchangeable when they actually carry different meanings: "absent/not provided" vs "explicitly cleared" vs "present but empty". Before writing a null/undefined guard, confirm exactly which sentinel the data source uses for each case, especially across serialization boundaries (protobuf, JSON-RPC, hand-rolled schemas) where a decoder may turn an omitted field into `[]` or `null` instead of `undefined`.

Concretely:
- Don't assume `??` catches every "missing" case. `images ?? retry.images` failed because protobuf decodes an omitted `images` field as `[]`, not `undefined`/`null`, so the fallback never ran. Check emptiness explicitly when that's the real intent: `images?.length ? images : retry.images`.
- Don't narrow a loop/guard only against `undefined` when the wire format can also send `null`. An MCP `nextCursor` of `null` passed `cursor !== undefined` and caused an infinite pagination loop; validate the actual expected type (`typeof cursor === "string" ? cursor : undefined`).
- Keep `null` and `undefined` distinct when they mean different things to the callee. A reasoning-context parameter used `null` to mean "explicitly unlisted model" vs the default-triggering `undefined`; collapsing the signature to only `| undefined` silently changed behavior. Similarly, an API's `metadata: null` meant "clear the field" while an omitted `metadata` meant "leave unchanged" — encoding both as the same JSON shape turned a clear into a no-op.
- Match "is present" checks to what they're actually guarding. `callerInitialMessages !== undefined` treated a caller-supplied empty array the same as "has messages", which fed into logic that wanted `.length > 0`. Pick the check that matches the real condition, not just the type.
- Never silently fall through an unexpected `null`/`undefined` from a call that is documented to always produce a value (e.g. `ensureSessionPersisted` returning no artifacts). If that state should be impossible, throw explicitly instead of letting the code continue down a path that assumes the value exists.

When writing or reviewing null-handling code, ask: what are *all* the possible "empty" representations this value can take (not just the ones in the type signature), and does each one map to the behavior you intend? Add a regression test for each distinct empty/absent state (null, undefined, `[]`, `""`) that has different intended behavior.