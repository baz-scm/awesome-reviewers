---
title: Make naming semantics explicit
description: 'Prefer identifier names that encode the real intent and lifecycle semantics,
  and keep names consistent across the codebase.


  Apply these rules:

  - Align with existing canonical types/names: if there’s a shared naming source (e.g.,
  `ClientName`), reuse it rather than inventing near-duplicates.'
repository: cline/CLINE
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 70839
---

Prefer identifier names that encode the real intent and lifecycle semantics, and keep names consistent across the codebase.

Apply these rules:
- Align with existing canonical types/names: if there’s a shared naming source (e.g., `ClientName`), reuse it rather than inventing near-duplicates.
- Avoid vague booleans and negation-y flags. If a boolean actually represents a domain “mode/state”, use an explicit enum/union/string type instead of `true/false`.
- For telemetry and APIs, treat property/key names as part of the contract: renames must be propagated to all call sites (positional args won’t be caught by TS).
- When renaming something for semantics (e.g., lifecycle phase labels), ensure the name matches what the code truly claims (e.g., “retried” meaning “the retry process ran”, not “the run succeeded”).

Example (boolean → explicit state):
```ts
type LoadOrigin = 'userInitiated' | 'background';

function load(refresh: boolean, origin: LoadOrigin) {
  if (origin === 'background') {
    // background checks
  }
  // ...
}
```

Example (telemetry contract):
```ts
captureCheckpointUsage(ulid, action, durationMs); // ensure callers pass ulid, not taskId
```

This improves searchability, reduces misinterpretation, and prevents subtle contract breaks caused by naming drift.