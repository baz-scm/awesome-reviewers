---
title: Distinguish null from absence
description: Treat `null`, `undefined`, and "key omitted" as distinct states whenever
  they can carry different meaning, and validate that distinction explicitly rather
  than trusting compile-time types or convenient operators to collapse them correctly.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70965
---

Treat `null`, `undefined`, and "key omitted" as distinct states whenever they can carry different meaning, and validate that distinction explicitly rather than trusting compile-time types or convenient operators to collapse them correctly.

Concretely:
- At system boundaries (JSON over stdio/HTTP, protobuf, external APIs), do not assume a value matches its TypeScript type. A server can send `nextCursor: null` even though your interface says `string | undefined`; narrow and validate at runtime instead of comparing raw values against `undefined`:
  ```ts
  cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
  ```
- Be careful with `??` and default parameters: `??` only falls through on `null`/`undefined`, not on empty strings or empty arrays, so `images ?? retry.images` keeps an empty-but-present array. Prefer an explicit emptiness check (`images?.length ? images : retry.images`) when "present but empty" and "absent" mean different things. Likewise, default parameter values swallow `undefined` but not `null`, so a function signature typed as `T | undefined` will silently misbehave if callers can legitimately pass `null` — type and handle both if both are reachable.
- When a value can mean several different things (not-yet-loaded vs. explicitly-empty vs. default vs. cleared), give each state its own representable value and handle them separately instead of collapsing them into one falsy/sentinel check. For example, a "loading" state should not be indistinguishable from "use the default."
- When forwarding or re-encoding a nullable field through another layer (e.g. `metadata: null` meaning "clear this field" vs. omitting the key meaning "leave it unchanged"), confirm the downstream decoder preserves that distinction; a naive rewrite can turn an explicit clear into a no-op or vice versa.
- Never let a fallback/defaulting helper's rare null-ish return be assumed non-null just because it "normally" throws or assigns a value — if the resulting state is unsafe, throw explicitly rather than falling through.
- Don't treat an absent optional field (e.g. a missing `accountId`) as a positive state change; absence should mean "no information," not "something switched."

Add regression tests that specifically exercise the `null`, `undefined`, and omitted-key cases for any field whose nullability has distinct meaning, since these are the cases most likely to be missed by type-level reasoning alone.