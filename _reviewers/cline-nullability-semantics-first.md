---
title: Nullability semantics first
description: 'Treat null/undefined/omitted values as distinct states and make that
  distinction explicit in both types and request/transition logic.


  Apply these rules:'
repository: Cline/Cline
label: Null Handling
language: TypeScript
comments_count: 10
repository_stars: 70840
---

Treat null/undefined/omitted values as distinct states and make that distinction explicit in both types and request/transition logic.

Apply these rules:
1) Match runtime normalization with types
- If code normalizes `null` internally, the exported/annotated signature must reflect `null` (not just `undefined`).
- Prefer normalizing at the boundary: convert incoming optional fields into a small, explicit set of internal states.

2) Encode “present only in some phase” in TypeScript
- Don’t rely on “optional” fields that are only valid in certain lifecycle moments. Use a discriminated union / gated shape so invalid reads are type errors.

3) Don’t silently fall back on missing required context
- If an optional value is required to choose the correct path (e.g., cloud requires a repo; auth hint requires matching providerAuth), fail the operation or disable the action rather than picking a default.

4) Make reset intent explicit in API payloads
- When resetting a setting, send an explicit null (or explicit reset literal) if that’s the contract; avoid omitting the field when “reset” is intended.

Example pattern (normalize + type-gate + explicit reset):
```ts
// 1) Presence is phase-gated: invalid combinations are unrepresentable
type BeforeRun = { kind: 'beforeRun'; entry: 'run' | 'continue'; snapshot: Snap };
type AfterRun = { kind: 'afterRun'; snapshot: Snap };

type Ctx = BeforeRun | AfterRun;

function run(ctx: Ctx) {
  // OK: only exists for beforeRun
  if (ctx.kind === 'beforeRun') {
    handleEntry(ctx.entry);
  }
}

// 2) Normalize null vs undefined at the boundary
type Patch = { baseUrl: string | null | undefined };
function toConnectionPatch(p: Patch) {
  if (p.baseUrl === undefined) return undefined;      // omit: no change
  return { baseUrl: p.baseUrl };                     // null => explicit reset
}

// 3) Avoid silent fallback
function resolveMode(requested: 'cloud' | 'local', repoUrl?: string) {
  if (requested === 'cloud' && !repoUrl) throw new Error('repoUrl required for cloud');
  return requested;
}
```

Following this consistently prevents stale state, accidental “empty means nothing” bugs, and incorrect defaults caused by ambiguous null/undefined handling.