---
title: Semantics-First Naming
description: Adopt a naming standard where identifiers communicate the *real* domain
  meaning, stay consistent with shared types/conventions, and don’t mislead API consumers.
repository: cline/cline#v20
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 70886
---

Adopt a naming standard where identifiers communicate the *real* domain meaning, stay consistent with shared types/conventions, and don’t mislead API consumers.

Guidelines
1) Prefer semantic, positive names over vague booleans/negation
- Avoid parameters like `background` that require `!background` to understand intent.
- If the concept has more than a yes/no meaning, model it as an enum-like string (e.g. `entry: "run" | "continue"`, `promptState: "seeded" | "not_seeded"`) rather than `boolean`.

Example
```ts
// before
function load(refresh: boolean, background = false) {
  if (!background) { /* ... */ }
}

// after
function load(refresh: boolean, userInitiated = false) {
  if (userInitiated) { /* ... */ }
}
```

2) Keep names tied to shared types—don’t “escape hatch” with `string`
- When there’s a shared union/type (e.g. `ClientName`), use it directly so all valid values are representable and typechecked.
- If a new host/client exists, add it to the shared type rather than letting the mismatch leak into local string types.

3) If you rename an identifier/property, update all call sites and preserve semantic format
- Renaming `taskId` → `ulid` is not just cosmetic: every caller must pass the correct identifier type/value.
- Don’t rely on positional arguments for semantic identifiers; prefer named parameters/objects when the risk of swapping/positional mismatch is high.

4) Avoid jargon and ambiguous API names
- Ensure exported functions are “obvious to call”: either expose a single primary function or choose names that strongly indicate what callers should use.
- If terminology is domain-specific (“pointer/save/dangling”), either define it up front (file-level comment) or pick more conventional words.

5) Follow existing casing/key conventions based on origin
- For structured payloads (telemetry/event properties), use the same casing rules already established in the codebase (e.g. keys derived from the caller’s `context` stay camelCase; keys added by the telemetry envelope/global enrichment stay snake_case).

Rule of thumb
- A good name answers: “What is this exactly?” without needing negation, jargon knowledge, or cross-referencing another file’s implementation.