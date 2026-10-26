---
title: Semantic Naming Standards
description: 'Identifier names should encode meaning and usage intent.


  Guidelines:

  1) Prefer semantically accurate names over vague booleans/flags

  - If a boolean isn’t clearly domain-descriptive, rename it to what it *means* (not
  how it’s “used”). If needed, replace the boolean with a string-enum that describes
  the state positively.'
repository: cline/cline#v22
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70886
---

Identifier names should encode meaning and usage intent.

Guidelines:
1) Prefer semantically accurate names over vague booleans/flags
- If a boolean isn’t clearly domain-descriptive, rename it to what it *means* (not how it’s “used”). If needed, replace the boolean with a string-enum that describes the state positively.

Example:
```ts
// Avoid vague: background / !background
async function load(refresh: boolean, background = false) {
  if (!background) userInitiated = true;
}

// Prefer semantic: userInitiated
async function load(refresh: boolean, userInitiated = false) {
  if (userInitiated) {/* first spinner logic */}
}
```

2) Avoid ambiguous booleans in data models
- When a field describes a domain scenario (e.g., “prompt came from host vs run input”), model it as a string-enum (or similarly explicit type) rather than a boolean that requires negation to understand.

3) Align with canonical types/unions already used in the codebase
- If a canonical name/type exists (e.g., `ClientName`), reuse it. Don’t introduce parallel naming schemes or rely on string “escape hatches” when unions already exist.

4) Keep identifier formats consistent across event/telemetry surfaces
- If you rename an ID key (e.g., `taskId` → `ulid`), update all call sites and ensure each event uses the correct identifier under the same property key; inconsistent key naming breaks consumers that join on IDs.

5) Make exported APIs hard to misuse
- If there are multiple related functions, prefer exporting one “obvious” entry point. If multiple exports are required, names and/or documentation must make the selection criteria unmistakable.

6) Follow casing/contract conventions by identifier origin
- If a system follows “caller-supplied context keys are camelCase, envelope/global enrichment are snake_case”, keep that rule; don’t rename keys solely for style if it would misrepresent origin/contract.