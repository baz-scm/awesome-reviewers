---
title: Null vs Omit Contracts
description: Treat `null`, `undefined` (omitted), and “empty but present” as distinct
  *semantic signals*—and make the distinction explicit at API/protocol boundaries.
repository: cline/cline#v19
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70885
---

Treat `null`, `undefined` (omitted), and “empty but present” as distinct *semantic signals*—and make the distinction explicit at API/protocol boundaries.

Apply this standard:
- Define the meaning of each state in the contract: **omit** (keep existing), **null** (clear/reset), **undefined** (not provided), **empty** (intentionally empty).
- Normalize at the boundary as early as possible (e.g., in request builders/transport adapters) so the rest of the code never guesses.
- Preserve “clear” semantics end-to-end: if the storage/protocol decodes `null` as omit, encode the clear in the form the persistence layer expects.
- Don’t rely on `??` when empty arrays/strings are meaningful; distinguish “missing” from “present empty”.
- Add tests for transitions: custom value → clear to default, and “missing field” vs “explicit empty/null”.

Examples:
```ts
// 1) When null means 'clear/reset', send an explicit null to the live contract
// so the system can revert to the manifest default.
await updateConnection({ baseUrl: null });

// 2) When schema advertises string but upstream sends null, normalize null -> omit
// for operations where null should mean 'not provided'.
function normalizeOldText(oldText: string | null | undefined) {
  return oldText === null ? undefined : oldText;
}

// 3) When omitted images decodes as [] but [] is still a meaningful “present empty”,
// prefer a length check instead of nullish coalescing.
const finalImages = images?.length ? images : retry.images;

// 4) When persistence layer would treat metadata: null as omit, preserve clear
// using the encoding that means 'clear', not 'no-op'.
await hubClient.command("session.update", {
  sessionId,
  ...(updates.metadata === undefined ? {} : updates.metadata),
});
```

Rule of thumb: if a field controls behavior (clear vs keep, reset vs default, missing vs intentionally empty), write code and tests that prove the chosen representation (`null`/omit/undefined/empty) produces the intended effect.