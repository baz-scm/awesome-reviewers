---
title: Null Semantics Discipline
description: Ensure your code treats `null`, `undefined`, “omitted”, and “empty” as
  distinct meanings—especially across serialization boundaries—and encode those meanings
  explicitly.
repository: cline/CLINE
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70839
---

Ensure your code treats `null`, `undefined`, “omitted”, and “empty” as distinct meanings—especially across serialization boundaries—and encode those meanings explicitly.

Apply these rules:
- **Normalize at boundaries** (parsers, protobuf builders, RPC payloads): convert provider/model quirks (e.g., `null` meaning “not provided”) into consistent internal representations.
- **Define precedence with helpers**: if multiple flags exist, centralize the rule (e.g., disabled vs enabled) in a single function and reuse it.
- **Don’t use `??` when omission and empty are different intents**: protobuf and decoders may turn an omitted field into `[]`. When intent depends on “provided vs not provided”, decide using `length`/presence checks, not only nullish coalescing.
- **Model illegal field presence in TypeScript**: when a field is “only set for beforeRun” (or similar), represent that in the type so misuse is caught by the compiler.
- **Test the edge conversions**: add tests for cases like `null` vs `{}` encoding, `undefined` swallowed by defaults, and “missing repoUrl must not silently fall back”.

Example (flag precedence + null normalization):
```ts
export function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  return data.disabled === true || (data.disabled === undefined && data.enabled === false)
}

// Normalize model-sent null to omission
function normalizeOptionalString(v: unknown): string | undefined {
  return typeof v === "string" ? v : undefined // treat null/undefined/other as omitted
}
```