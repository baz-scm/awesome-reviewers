---
title: Semantic, Consistent Naming
description: 'Adopt naming that is (a) semantically clear, (b) consistent across all
  call sites/consumers, and (c) unambiguous for public APIs.


  **1) Avoid vague boolean/flag names**'
repository: cline/cline#v19
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 70885
---

Adopt naming that is (a) semantically clear, (b) consistent across all call sites/consumers, and (c) unambiguous for public APIs.

**1) Avoid vague boolean/flag names**
- If a boolean hides domain meaning, rename it to a positive, descriptive concept.
- If the state has more than two meaningful outcomes, prefer a string-literal union/enum.

```ts
// Prefer positive, domain-meaning naming
async function load(userInitiated: boolean, /* ... */) {
  if (userInitiated) { /* show initial spinner logic */ }
}

type EntryKind = 'run' | 'continue';
function beforeRun(ctx: { entry?: EntryKind }) { /* ... */ }
```

**2) Keep renamed identifiers consistent across consumers**
- When renaming event properties/parameters (e.g., telemetry), update *all* call sites.
- Don’t introduce naming drift between producers and the downstream join/aggregation keys.

**3) Use shared naming types where they already exist**
- For identifiers like “client names”, use the centralized union/type from the shared context module rather than defining ad-hoc variations.

**4) Make public exports easy to choose**
- If two exported functions are related, ensure callers can tell which one to use.
- Prefer exporting a single canonical function; otherwise, use names (and comments) that strongly indicate intent/selection criteria.

This standard prevents: ambiguous flags, hidden negation semantics, inconsistent event/property keys, and confusing “which function should I call?” APIs.