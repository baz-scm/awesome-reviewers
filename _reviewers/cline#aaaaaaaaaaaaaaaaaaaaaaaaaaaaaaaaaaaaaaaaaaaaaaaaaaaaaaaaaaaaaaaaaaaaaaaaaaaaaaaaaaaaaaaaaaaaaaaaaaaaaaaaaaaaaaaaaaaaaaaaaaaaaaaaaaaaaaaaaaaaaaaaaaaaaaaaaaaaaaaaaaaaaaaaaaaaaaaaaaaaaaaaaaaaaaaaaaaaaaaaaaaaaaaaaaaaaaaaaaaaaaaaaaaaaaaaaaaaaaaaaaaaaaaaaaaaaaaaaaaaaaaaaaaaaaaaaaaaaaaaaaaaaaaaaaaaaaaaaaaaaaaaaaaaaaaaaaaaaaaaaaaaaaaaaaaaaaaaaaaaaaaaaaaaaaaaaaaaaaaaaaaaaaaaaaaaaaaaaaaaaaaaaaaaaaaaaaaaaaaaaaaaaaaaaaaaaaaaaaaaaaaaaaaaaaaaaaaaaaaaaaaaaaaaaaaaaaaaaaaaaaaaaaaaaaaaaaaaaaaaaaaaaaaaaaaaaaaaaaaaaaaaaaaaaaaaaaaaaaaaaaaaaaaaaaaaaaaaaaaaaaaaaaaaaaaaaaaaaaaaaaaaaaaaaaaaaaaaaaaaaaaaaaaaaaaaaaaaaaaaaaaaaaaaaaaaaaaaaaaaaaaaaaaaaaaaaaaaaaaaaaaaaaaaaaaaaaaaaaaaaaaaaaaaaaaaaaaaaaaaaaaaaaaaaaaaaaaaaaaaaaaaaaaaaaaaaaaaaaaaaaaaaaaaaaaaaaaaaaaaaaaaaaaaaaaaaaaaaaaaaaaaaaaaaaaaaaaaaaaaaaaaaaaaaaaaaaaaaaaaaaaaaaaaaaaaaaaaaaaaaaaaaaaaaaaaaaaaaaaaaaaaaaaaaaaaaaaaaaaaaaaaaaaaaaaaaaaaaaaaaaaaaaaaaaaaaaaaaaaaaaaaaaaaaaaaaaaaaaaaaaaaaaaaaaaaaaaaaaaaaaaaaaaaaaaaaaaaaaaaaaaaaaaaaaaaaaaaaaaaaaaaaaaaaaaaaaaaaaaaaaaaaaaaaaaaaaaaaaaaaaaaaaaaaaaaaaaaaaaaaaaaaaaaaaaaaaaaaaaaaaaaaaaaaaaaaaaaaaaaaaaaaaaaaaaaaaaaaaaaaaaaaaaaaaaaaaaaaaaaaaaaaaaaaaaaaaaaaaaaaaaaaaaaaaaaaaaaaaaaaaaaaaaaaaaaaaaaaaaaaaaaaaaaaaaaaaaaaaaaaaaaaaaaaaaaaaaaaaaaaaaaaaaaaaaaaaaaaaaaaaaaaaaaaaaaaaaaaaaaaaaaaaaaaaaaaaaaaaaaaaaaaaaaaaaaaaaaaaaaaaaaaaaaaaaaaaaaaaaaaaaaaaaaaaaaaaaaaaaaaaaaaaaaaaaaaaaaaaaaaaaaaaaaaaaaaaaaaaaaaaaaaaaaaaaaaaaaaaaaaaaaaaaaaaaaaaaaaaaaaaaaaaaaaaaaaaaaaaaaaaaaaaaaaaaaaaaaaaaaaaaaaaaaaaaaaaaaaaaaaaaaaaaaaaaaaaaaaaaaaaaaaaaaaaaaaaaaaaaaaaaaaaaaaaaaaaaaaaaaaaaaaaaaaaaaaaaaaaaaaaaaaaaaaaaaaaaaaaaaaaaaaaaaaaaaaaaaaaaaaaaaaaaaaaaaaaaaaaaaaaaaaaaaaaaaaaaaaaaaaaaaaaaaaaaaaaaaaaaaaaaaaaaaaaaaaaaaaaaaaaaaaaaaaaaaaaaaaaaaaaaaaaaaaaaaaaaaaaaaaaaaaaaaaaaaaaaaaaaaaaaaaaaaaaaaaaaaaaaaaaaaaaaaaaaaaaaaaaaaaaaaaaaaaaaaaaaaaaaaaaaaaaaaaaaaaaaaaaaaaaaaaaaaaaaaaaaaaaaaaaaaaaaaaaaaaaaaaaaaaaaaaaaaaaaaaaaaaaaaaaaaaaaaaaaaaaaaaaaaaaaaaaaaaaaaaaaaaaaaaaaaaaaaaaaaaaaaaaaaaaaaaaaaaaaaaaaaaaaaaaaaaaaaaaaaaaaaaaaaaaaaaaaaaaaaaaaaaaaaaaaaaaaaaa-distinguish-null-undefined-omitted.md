---
title: Distinguish null, undefined, omitted
description: 'When a field can be "not provided," "explicitly cleared," "still loading,"
  or "intentionally empty," treat these as distinct states rather than collapsing
  them into a single falsy/nullish check. Bugs repeatedly show up when these states
  get conflated across a boundary: serialization helpers that decode `null` the same
  as "absent" and silently turn an...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70967
---

When a field can be "not provided," "explicitly cleared," "still loading," or "intentionally empty," treat these as distinct states rather than collapsing them into a single falsy/nullish check. Bugs repeatedly show up when these states get conflated across a boundary: serialization helpers that decode `null` the same as "absent" and silently turn an explicit clear into a no-op, protobuf/JSON clients that encode "nothing provided" as `[]` instead of `undefined`/`null` (making `value ?? fallback` never trigger), JS default parameters that only fire on `undefined` and so swallow a deliberate `null` sentinel, and UI state that uses `null` to mean "loading" versus a separate "default/unset" option.

To apply this:
- When adding or changing an optional/nullable field, explicitly enumerate every state it can carry (not-set, explicit empty, explicit clear/reset, loading, etc.) and decide how each one should be encoded and decoded at the boundary.
- Do not rely on `??`, `||`, or default parameters to detect "no value provided" unless you've confirmed the actual wire/runtime representation matches (e.g. check `.length` for collections, check for `null` specifically if that's the real "unset" encoding).
- If `null` and `undefined` carry different meanings (e.g. "clear this field" vs "leave unchanged"), make sure every layer (serializer, store, RPC/protobuf schema, function signature) preserves that distinction instead of normalizing one into the other.
- Add a regression test for each meaningfully distinct state transition (e.g. custom value → explicit clear → default; retry with no new attachments vs retry with attachments; loading vs "no value saved").

Example of the failure mode to avoid:
```ts
// BAD: null and "omitted" both decode to the same thing downstream,
// so an explicit clear silently becomes a no-op.
const metadata: Record<string, unknown> = { ...(updates.metadata ?? {}) };

// GOOD: forward the caller's intent (including an explicit null) untouched,
// and encode "clear" distinctly from "omitted/unchanged".
...(updates.metadata !== undefined ? { metadata: updates.metadata } : {})
```