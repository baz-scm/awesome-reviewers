---
title: Intentional Null Semantics
description: When data crosses boundaries (protobuf/JSON, schema validation, persistence/daemon,
  RPC), treat `undefined`, explicit `null`, and empty values as distinct. Don’t rely
  on language-level defaults—choose/normalize the value that matches the backend’s
  meaning.
repository: cline/cline#v18
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70884
---

When data crosses boundaries (protobuf/JSON, schema validation, persistence/daemon, RPC), treat `undefined`, explicit `null`, and empty values as distinct. Don’t rely on language-level defaults—choose/normalize the value that matches the backend’s meaning.

Apply:
1) Prefer omission for “not provided”, explicit `null` only when the contract defines it as “clear/reset”.
2) If a decoder turns “omitted” into an empty value (e.g., `[]`), use “only replace when actually present” logic—typically `??` (nullish coalescing) or a presence flag.
3) If upstream models may send `null` for fields you want to treat as “optional/omitted”, normalize `null` to `undefined`/omit before sending to the backend.
4) Encode conditional presence in types (so “only set in beforeRun” fields can’t be read as always-present).
5) Add tests for the 3 cases: omitted vs `null` vs empty string/array.

Example pattern (preserve prior attachments unless the new payload truly provides them):
```ts
// images?: string[]
// If protobuf omits images, it may decode as []
const nextImages = images?.length ? images : retry.images; // choose contract-true semantics
await initTask(retry.prompt, nextImages, files, /*...*/);
```

Example pattern (normalize `null` to omission for request fields that should be “unset”):
```ts
type Edit = { old_text?: string | null };
function normalizeEdit(e: Edit): { old_text?: string } {
  return e.old_text == null ? {} : { old_text: e.old_text };
}
```

This prevents subtle no-ops and unintended overwrites caused by null vs omitted decoding differences (and keeps runtime behavior aligned with the intended contract).