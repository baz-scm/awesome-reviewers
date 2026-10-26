---
title: Null and Missing Semantics
description: When handling potentially-null/optional fields, treat `null`/`undefined`/empty/`false`
  as distinct meanings and make that explicit in both types and runtime normalization—especially
  across parsing, schema validation, and persistence/serialization boundaries.
repository: cline/cline#v10
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 70869
---

When handling potentially-null/optional fields, treat `null`/`undefined`/empty/`false` as distinct meanings and make that explicit in both types and runtime normalization—especially across parsing, schema validation, and persistence/serialization boundaries.

**What to do**
1. **Define semantics** for each boundary field: e.g. `undefined` = “unspecified”, `null` = “explicit clear”, empty list/string = “explicit empty”, `false` = “explicit disabled”.
2. **Normalize at the boundary** (parsers / API handlers / LLM/tool payload decoding) into a single internal representation.
3. **Align TypeScript signatures with runtime behavior** so defaults don’t accidentally swallow explicit `null`/unset intent.
4. **Preserve wire encoding** for persistence: if `{}` is the “clear” signal today, don’t change it to `null` (or vice-versa) without tests.
5. **Add regression tests** for explicit `null`/`false`/empty vs omitted cases.

**Example patterns**
```ts
// 1) Normalize model null -> omission (runtime), while advertising string in schema
function normalizeOptionalString(value: unknown): string | undefined {
  return typeof value === "string" ? value : value === null ? undefined : undefined;
}

// 2) Keep signature aligned with normalization (avoid undefined/null mismatch)
type ReasoningIntent = { reasoning?: string | null };
function resolveIntent(req: ReasoningIntent): "none" | "high" | undefined {
  // If req.reasoning explicitly null means "none", handle it directly.
  if (req.reasoning === null) return "none";
  if (req.reasoning === undefined) return undefined; // omitted
  return req.reasoning;
}

// 3) Preserve persistence semantics: "clear" must serialize the same way
type Update = { metadata?: Record<string, unknown> | null };
function encodeUpdate(u: Update) {
  if (u.metadata === null) return { metadata: {} }; // explicit-clear encoding
  if (u.metadata === undefined) return {};           // omitted
  return { metadata: u.metadata };                 // set
}
```

If you’re ever tempted to “simplify” by folding `null` into omission or by rewriting persistence payloads, stop and verify the receiver’s interpretation with targeted tests.