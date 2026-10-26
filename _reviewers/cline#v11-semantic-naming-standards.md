---
title: Semantic Naming Standards
description: 'Adopt naming that is (a) consistent with existing canonical types, (b)
  semantically self-evident, and (c) correct for the underlying value format.


  Checklist:'
repository: cline/cline#v11
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70871
---

Adopt naming that is (a) consistent with existing canonical types, (b) semantically self-evident, and (c) correct for the underlying value format.

Checklist:
1) Prefer canonical names/types when they already exist
- If the codebase defines a canonical identifier (e.g., `ClientName`), new exported/client-related types should align with it to avoid drift.

2) Avoid vague boolean flags; model domain meaning in the name
- If a boolean represents a domain situation, rename to the actual situation or replace it with a positive enum-like string.
- Prefer positive naming over negation (i.e., make the “true case” meaningful).

3) Ensure names match identifier formats across call sites/events
- If you rename a property to reflect a different identifier format (e.g., `taskId` → `ulid`), update all call sites and keep event property semantics consistent.

4) Follow casing conventions deterministically (by origin)
- Example rule: “caller-supplied context keys use camelCase; envelope/global-enrichment keys use snake_case.” Don’t mix conventions within the same origin.

5) Make exported APIs obvious to choose
- Avoid multiple public functions with confusingly similar purposes unless the naming makes the intended choice immediately clear.

Example (boolean → semantic string):
```ts
// Before
type Entry = { entry?: 'run' | 'continue'; promptSeeded?: boolean }

// After (positive, non-boolean)
type Entry = {
  entry?: 'run' | 'continue'
  promptSeededState?: 'seeded' | 'written'
}
```