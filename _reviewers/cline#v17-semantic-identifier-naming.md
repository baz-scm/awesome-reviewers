---
title: Semantic Identifier Naming
description: 'Use naming that makes the data’s meaning and origin obvious—and keep
  it consistent with existing domain conventions.


  **Standards**

  1. **Prefer positive, semantic names over vague booleans**'
repository: cline/cline#v17
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70883
---

Use naming that makes the data’s meaning and origin obvious—and keep it consistent with existing domain conventions.

**Standards**
1. **Prefer positive, semantic names over vague booleans**
   - If a boolean only exists to negate behavior, name it by the behavior/intent it represents.
   - If the domain is effectively more than two states, prefer an enum/string union over `true/false`.
2. **Align identifiers with existing shared types/values**
   - When a repo/host/client id already has a canonical type (e.g., a `ClientName` union), reuse it rather than inventing parallel names.
3. **Make public exports hard to misuse**
   - If multiple functions exist, names must clearly indicate which one to call. If there’s a “default correct” choice, export only that (and keep others internal or clearly test-only).
4. **Propagate renames to avoid silent semantic drift**
   - When renaming telemetry/event keys or parameters, update every call site and ensure downstream consumers expect the new identifier.
5. **Keep casing consistent by key origin/source**
   - Don’t mix conventions accidentally (e.g., caller `context` keys stay camelCase; telemetry envelope/global enrichment keys stay snake_case).
6. **Avoid jargon unless it’s precisely defined**
   - Use plain, descriptive terms; if special terminology is required, document it once at file-level or in the function docs.

**Examples**
```ts
// 1) Avoid negated / vague boolean intent
const load = async (refresh: boolean, userInitiated = false) => {
  if (userInitiated) showSpinner();
};

// 2) Prefer enums over booleans when domain is “state”
export interface AgentRunLifecycleContext {
  entry?: 'run' | 'continue';
  // instead of promptSeeded?: boolean
  promptSource?: 'seeded' | 'written';
}

// 3) Telemetry rename must be end-to-end
// captureCheckpointUsage(ulid, ...) must be called with ulid everywhere,
// not taskId, or your event schema becomes internally inconsistent.
```

Apply this checklist during review: does the name tell you *what it is*, *why it exists*, and *where it comes from*—without reading the implementation? If not, rename (or change the type) until it does.