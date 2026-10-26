---
title: Normalize nullable inputs
description: 'Treat `null`/`undefined`/“field omitted” as distinct states and normalize
  them at boundaries so internal logic never has to guess.


  Practical rules:

  - Define canonical semantics + precedence for legacy/variant inputs (e.g., `disabled`
  wins over `enabled: false`).'
repository: cline/cline#v28
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70892
---

Treat `null`/`undefined`/“field omitted” as distinct states and normalize them at boundaries so internal logic never has to guess.

Practical rules:
- Define canonical semantics + precedence for legacy/variant inputs (e.g., `disabled` wins over `enabled: false`).
- Normalize model/schema differences at the edges (e.g., accept `null` in incoming payloads, but convert it to omission before business logic).
- Distinguish “omitted” vs “explicit empty” when wire formats coerce values (e.g., protobuf decoding omitted `images` into `[]`).
- Prevent accidental NULL injection caused by contract mismatches (e.g., wrong named-parameter tokens in SQL bindings).
- After state is null/undefined’d (e.g., reset), update dependent derived state immediately.

Examples:

1) Distinguish omitted vs explicit empty
```ts
// If retry carried attachments but the incoming retry had `images: []` due to decoding,
// keep the original attachments unless the user actually provided non-empty images.
const finalImages = images?.length ? images : retry.images;
await initTask(retry.prompt, finalImages, files, undefined, undefined, retry.cloudTarget);
```

2) Normalize `null` to omission
```ts
// Accept null from some models, but treat it as “not provided” internally.
function normalizeOldText(oldText: string | null | undefined): string | undefined {
  return oldText === null ? undefined : oldText;
}

const oldTextNormalized = normalizeOldText(payload.old_text);
// use `oldTextNormalized` so create/insert operations don’t accidentally set null
```

3) Avoid accidental NULL in SQL named params
```ts
// Bun requires exact named tokens; unprefixed keys bind as NULL.
const row = nextDueRun.get({ ":now": referenceIso, ":capacity": cap });
```