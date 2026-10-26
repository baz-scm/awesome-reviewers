---
title: Normalize null semantics
description: When data crosses a boundary (serialization, persistence, protocol, config
  parsing, UI↔host), treat `null`, `undefined` (omitted), and “empty” as different
  meanings. Normalize explicitly at the boundary and encode precedence rules so resets/clears,
  omissions, and legacy fallbacks don’t silently change behavior.
repository: cline/cline#v5
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70864
---

When data crosses a boundary (serialization, persistence, protocol, config parsing, UI↔host), treat `null`, `undefined` (omitted), and “empty” as different meanings. Normalize explicitly at the boundary and encode precedence rules so resets/clears, omissions, and legacy fallbacks don’t silently change behavior.

Apply:
- **Make intent explicit**: use `null` only when the target contract defines “clear/reset”, and use omission when you mean “leave unchanged”.
- **Encode precedence** (don’t rely on truthiness): e.g., `disabled` wins over legacy `enabled`.
- **Fix types + defaults**: if runtime distinguishes `null` vs `undefined`, the function signature and defaulting must reflect it (otherwise defaults can swallow `undefined` and mis-route logic).
- **Account for wire-format defaults**: e.g., if protobuf decodes an omitted field as `[]`, then `images ?? retry.images` may be wrong—use a presence/length rule that matches the intended semantics.

Example patterns:

```ts
// 1) Precedence: disabled wins
export function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  if (typeof data.disabled === "boolean") return data.disabled
  return data.enabled === false
}

// 2) Clear vs omit: if persistence decodes null as “omitted”, don’t use null for clears.
function encodeSessionUpdateForClear(prev: object) {
  return { metadata: {} } // use the encoding the persistence layer treats as an actual clear
}

// 3) Signature correctness: don’t let undefined fall into a default that changes behavior.
function resolveEffort(req: { effort?: string | null }, ctx: { /*...*/ }) {
  // Normalize explicitly
  const effort = req.effort ?? null
  if (effort === null) return "none"
  return effort
}

// 4) Wire-format default: omitted images => []
function pickRetryImages(webviewImages: string[] | undefined, retryImages: string[]) {
  // If webview explicitly sends [] (omitted decoded), preserve retryImages only when webview intended “none provided”
  // (choose the rule that matches your contract; here: treat empty array as “omitted/none provided”)
  return webviewImages && webviewImages.length > 0 ? webviewImages : retryImages
}
```

Rule of thumb: add small tests for transitions like **custom→default**, **clear→no-op**, and **null/omitted→wire defaults** so future refactors can’t accidentally swap semantics.