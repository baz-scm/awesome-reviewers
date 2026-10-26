---
title: Semantic Naming Standards
description: Adopt a naming standard where identifiers encode meaning (not implementation),
  stay stable across lifetimes, and follow the project’s casing/key provenance rules.
repository: cline/cline#v4
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Adopt a naming standard where identifiers encode meaning (not implementation), stay stable across lifetimes, and follow the project’s casing/key provenance rules.

Rules:
1) Encode intent in names (avoid vague booleans)
- Prefer parameter/flag names that answer “what does this tell the caller?” not “what does this condition do internally?”.
- Avoid negative/ambiguous booleans when the domain is really multi-state.
  - Prefer enums/union strings with positive meaning over boolean + negation.

2) Ensure names match the identifier format
- If a parameter/property is named `ulid`, the value passed must be a ULID (not a task id). Don’t rely on positional renames; align call sites and payload keys.

3) Follow casing/key conventions by origin
- Apply casing based on where the key comes from.
  - Example policy: caller-supplied `context` keys use `camelCase`; telemetry/envelope/global-enrichment keys use `snake_case`.

4) Keep identity fields stable when referenced across time/UI actions
- For ids used by actions (Use/Send/Skip/Undo), define how they’re constructed so they remain consistent across the relevant window (e.g., per turn) and don’t “silently change meaning”.

5) Make public APIs obvious
- Prefer one main exported function that most callers should use.
- If multiple functions must be public, name them so the correct choice is self-evident, and document the decision criterion in the comment.

Example (before/after):
```ts
// Before: vague and semantics unclear
function load(refresh: boolean, background = false) { /* ... */ }

// After: naming ties to intent
function load(refresh: boolean, userInitiated: boolean = false) { /* ... */ }

// Before: boolean hides a multi-state concept
type Entry = { promptSeeded?: boolean };

// After: explicit, positive state
type Entry = { promptSource?: 'seeded' | 'written' };
```

Checklist for PR naming changes:
- Does the name state the caller-visible meaning?
- Can the type/value be mismatched with the name (e.g., `ulid` vs `taskId`)?
- Are casing/key conventions correct for the key’s origin?
- Are ids stable across the period other components depend on?
- Is there a clear “what should I call?” answer for public functions/types?