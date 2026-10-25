---
title: Semantic, Consistent Naming
description: 'Use naming that is semantically precise, consistent with existing conventions,
  and hard to misuse.


  **Rules**

  1. **Prefer existing vocabulary/types.** If the codebase already has a canonical
  type or naming scheme, align to it (e.g., client identifiers should use the established
  `ClientName` concept).'
repository: CLINE/cline
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70839
---

Use naming that is semantically precise, consistent with existing conventions, and hard to misuse.

**Rules**
1. **Prefer existing vocabulary/types.** If the codebase already has a canonical type or naming scheme, align to it (e.g., client identifiers should use the established `ClientName` concept).
2. **Avoid vague booleans.** If a boolean represents a concept with more than “true/false semantics” (or requires guessing what false means), rename to the positive meaning or replace with a string/enum.
3. **Make exported/public APIs self-selecting.** Public functions/types should clearly indicate when to call them. If multiple similar exports exist, consider exporting one obvious entry point; otherwise rename to strongly communicate the selection criteria.
4. **Keep event/property identifiers consistent end-to-end.** If you rename an event property key (e.g., from `taskId` to `ulid`), update all call sites and ensure the same logical property doesn’t contain mixed identifier formats across events.
5. **Avoid jargon in names and docs.** Use clear, positive language that matches the actual meaning; when domain terms are unavoidable, document what they mean and how callers should use them.

**Examples**
- Replace vague boolean with explicit meaning:
```ts
// Before: caller must infer what background=false means
load(refresh, background)

// After: name the intention/state
load(userInitiated, /* ... */)
```
- Replace boolean domain with an explicit state:
```ts
type Entry = "run" | "continue";

interface Ctx {
  entry?: Entry;
  promptSeeded?: "seeded" | "written"; // or a clearer two-state enum if applicable
}
```
- Ensure event property keys are consistent across producers:
```ts
// If you emit ulid under `ulid`, every call site should pass ulid there.
telemetry.capture({ properties: { ulid, /* ... */ } });
```