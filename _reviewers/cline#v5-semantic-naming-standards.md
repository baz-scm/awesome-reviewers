---
title: Semantic Naming Standards
description: 'Naming should encode *meaning* and *ownership*.


  Apply these rules:

  1) Prefer intent/state names over mechanism/flags

  - Avoid vague booleans like `background`.'
repository: cline/cline#v5
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 70864
---

Naming should encode *meaning* and *ownership*.

Apply these rules:
1) Prefer intent/state names over mechanism/flags
- Avoid vague booleans like `background`.
- Name by what the caller/user intended: e.g. `userInitiated`.

2) Replace ambiguous booleans with explicit state
- If the domain is more than “yes/no”, use a small string union or enum describing the positive state.

```ts
// Prefer:
type EntrySource = "run" | "continue";
interface LifecycleCtx {
  entry?: EntrySource;
  // instead of promptSeeded?: boolean
  promptSource?: "seeded" | "written";
}

// Over:
// promptSeeded?: boolean; // ambiguous "true/false" meaning
```

3) Make exported APIs discoverable
- If multiple exported functions do similar things, ensure names make it obvious which one callers should use—or export a single primary function and keep helpers private.

4) Reuse shared identifier types
- When a canonical type exists (e.g., a shared `ClientName`), don’t create parallel client identifiers; wire to the shared type so missing/host cases are enforced by the compiler.

5) Follow casing conventions based on data origin
- If keys come from the caller’s `context`, use camelCase.
- If keys are added by the telemetry/envelope/global enrichment layer, use snake_case.
- Don’t apply a blanket casing rule without checking ownership/source.