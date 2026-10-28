---
title: Disambiguate null vs empty
description: '`null`, `undefined`, and "empty" values (`""`, `[]`, `{}`) often carry
  distinct meanings and must never be assumed interchangeable. Several bugs in this
  codebase trace back to exactly this conflation: an MCP server sending `nextCursor:
  null` kept a pagination loop alive because `null !== undefined`; `images ?? retry.images`
  silently dropped a retried task''s...'
repository: cline/cline#`sleep 4`
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70979
---

`null`, `undefined`, and "empty" values (`""`, `[]`, `{}`) often carry distinct meanings and must never be assumed interchangeable. Several bugs in this codebase trace back to exactly this conflation: an MCP server sending `nextCursor: null` kept a pagination loop alive because `null !== undefined`; `images ?? retry.images` silently dropped a retried task's attachments because the webview sent `images: []` rather than omitting the field, so `??` (which only catches `null`/`undefined`) never fired; an explicit `baseUrl: null` "reset to default" had to be kept distinct from an empty-string override; a wire helper decoded a literal `null` as "field omitted," turning an explicit "clear this field" request into a silent no-op; and an archived conversation with zero messages needed to be treated the same as "no archive" rather than as a different, confusing state.

When writing or reviewing code that branches on presence/absence of a value:
- Decide explicitly what each of "not present," "explicitly null/cleared," "empty but present," and "default" means in your context, and say so in a comment if it's not obvious from the type.
- Don't trust external/untrusted input (server responses, wire protocols, user input) to only ever be `undefined` when "no value" is intended — narrow and validate it, e.g. `cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined`.
- When checking "did the caller actually supply something," cover every "nothing supplied" representation callers use instead of a single operator that only catches some of them:
  ```ts
  // Bug: a Retry click sends images: [] (not undefined), so ?? never
  // falls back and the original attachments are lost.
  await initTask(retry.prompt, images ?? retry.images, files)

  // Fix: treat "nothing meaningful supplied" explicitly.
  await initTask(retry.prompt, images?.length ? images : retry.images, files)
  ```
- When a serialization or transport layer encodes "omitted" and "explicit null" the same way, be deliberate about which one you need; encode "clear this field" with a value that survives the round trip (e.g. `{}` instead of a literal `null`), and add a regression test for that specific transition.
- If a value can legitimately be missing after a step that is supposed to guarantee it, fail loudly (throw) instead of silently falling through to code that assumes it's present.