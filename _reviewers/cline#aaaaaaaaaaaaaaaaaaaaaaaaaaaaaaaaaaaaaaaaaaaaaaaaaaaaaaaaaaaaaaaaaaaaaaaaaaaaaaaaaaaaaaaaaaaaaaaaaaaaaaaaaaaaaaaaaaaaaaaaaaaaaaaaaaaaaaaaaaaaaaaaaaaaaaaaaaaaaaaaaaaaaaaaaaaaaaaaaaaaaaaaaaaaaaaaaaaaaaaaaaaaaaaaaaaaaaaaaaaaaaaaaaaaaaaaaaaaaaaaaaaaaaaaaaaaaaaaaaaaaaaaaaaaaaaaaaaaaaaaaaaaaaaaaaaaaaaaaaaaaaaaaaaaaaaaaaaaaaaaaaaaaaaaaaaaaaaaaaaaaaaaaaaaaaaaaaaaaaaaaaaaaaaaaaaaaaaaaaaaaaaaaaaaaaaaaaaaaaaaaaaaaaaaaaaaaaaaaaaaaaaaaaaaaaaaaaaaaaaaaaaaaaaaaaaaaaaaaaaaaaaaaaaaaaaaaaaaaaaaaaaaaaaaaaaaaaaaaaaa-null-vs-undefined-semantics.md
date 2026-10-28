---
title: Null vs undefined semantics
description: Treat `null`, `undefined`, and "omitted" as distinct, deliberate signals
  rather than interchangeable stand-ins for "empty," and make the meaning of each
  explicit at every boundary where data crosses in or out (JSON parsing, schema validation,
  serialization, defaults).
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70964
---

Treat `null`, `undefined`, and "omitted" as distinct, deliberate signals rather than interchangeable stand-ins for "empty," and make the meaning of each explicit at every boundary where data crosses in or out (JSON parsing, schema validation, serialization, defaults).

Several bugs in this codebase came from losing or assuming the wrong distinction:
- A cursor field from an external server was checked with `!== undefined`, so a server sending `nextCursor: null` kept the pagination loop spinning forever. Narrow with an explicit type check instead of a loose equality test: `cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;`
- A function returning `null` on a rare failure path fell through into logic that assumed non-null, silently orphaning a session. When a code path can legitimately return `null`/`undefined`, handle it explicitly (throw or branch) rather than letting it fall through to logic written for the happy path.
- A UI selector collapsed "still loading" and "no value saved" into the same default, because it didn't reserve `null` to mean "loading." Use a dedicated sentinel per state when more than one "empty" state exists.
- A reset path needed `baseUrl: null` to mean "clear the override," distinct from `""` (an explicit empty string) and `undefined` (no change) — mixing these up silently reverted the wrong state or did nothing.
- A `null` sent by a model for an unused optional field was correctly treated as omitted at runtime, even though the schema advertises only a string — document this normalization explicitly in code comments so it isn't mistaken for a bug.
- A parameter default swallowed an explicit `undefined`, so `null` had to be used deliberately to signal "no value" through that boundary; when changing such a signature, keep the type and the call site in sync (e.g. `| null` must appear in both).
- Rewriting an update path to build a payload via spreads changed `metadata: null` (explicit "clear this field") into an omitted key, turning an intended clear into a no-op.

When writing code that accepts data from an external or untrusted source (API responses, model output, serialized payloads) or that builds/forwards such payloads, explicitly decide and document what `null`, `undefined`, and omission each mean, validate/narrow incoming values rather than trusting their declared type, and add a regression test for the "unexpected null" case alongside the happy path.