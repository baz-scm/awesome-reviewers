---
title: Null semantics and precedence
description: 'Treat `null`, `undefined` (omitted), and “empty” values as distinct
  states, and make the intended meaning explicit in code contracts and tests.


  Practical rules:'
repository: cline/cline#v11
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70871
---

Treat `null`, `undefined` (omitted), and “empty” values as distinct states, and make the intended meaning explicit in code contracts and tests.

Practical rules:
1) Define field semantics up front for each nullable/optional field:
   - **update**: new value provided
   - **clear**: explicit reset (often `null`)
   - **no-op**: field omitted/`undefined` (do not change stored value)
   - **empty**: empty string/array is still a real value, not the same as clear
2) Preserve the distinction through every layer (webview ↔ host ↔ runtime ↔ persistence). Don’t “encode clears” via `{}` or object spreads unless the receiving layer’s decoder treats it equivalently.
   - Example pattern: if the live connection expects an explicit reset, send `baseUrl: null` (not `""`), and ensure the persistence layer’s decoder maps `null`/`{}` as intended.
3) When multiple related boolean flags exist, implement deterministic precedence and test it.
   - e.g. `disabled: true` wins; only fall back to `enabled: false` when `disabled` is absent.
4) For arrays/optionals, choose fallback logic that distinguishes omitted vs intentionally empty.
   - If `[]` means “user provided no attachments”, do **not** fall back to prior values just because the array is empty.
5) Where possible, encode “field valid only in phase X” in TypeScript types (discriminated unions / construction-time guarantees) rather than relying on runtime `undefined` checks.

Example (precedence + omitted vs empty):
```ts
function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  // precedence: disabled wins
  return data.disabled === true || (data.disabled === undefined && data.enabled === false);
}

function pickImagesForRetry(imagesFromWebview: string[] | undefined, retry: { images: string[] }) {
  // if webview omitted images => undefined => use retry.images
  // if webview sent [] => keep []
  return imagesFromWebview === undefined ? retry.images : imagesFromWebview;
}
```

Adopt a short “null/undefined policy” comment near request/response shaping code (and a small unit test per edge case) so regressions like “clear becomes a no-op” or “empty treated as missing” don’t slip through.