---
title: Meaningful, consistent naming
description: 'Adopt naming rules that make identifiers semantically unambiguous, consistent
  in format, and discoverable.


  Guidelines

  1) Encode intent in names (especially booleans/flags)'
repository: cline/cline#v14
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70876
---

Adopt naming rules that make identifiers semantically unambiguous, consistent in format, and discoverable.

Guidelines
1) Encode intent in names (especially booleans/flags)
- Prefer names that describe the triggering actor or meaning.
- Example:
  - ✅ `load(userInitiated: boolean)`
  - ❌ `load(refresh: boolean, background = false)`

2) Follow casing conventions based on ownership/origin
- If the key is supplied by the caller in a `context` object, keep camelCase.
- If the key is added by the telemetry envelope/global enrichment, use snake_case.
- Don’t “half-normalize” just one key.
  - ✅ `context: { finishReason: ... }`
  - ✅ envelope: `{ finish_reason: ... }` (if the envelope is responsible)

3) Keep identifier formats consistent across renames
- If a property/parameter name changes from one identifier type to another, update all call sites and ensure the event schema uses the new identifier type consistently.
- Don’t mix “taskId” values under an “ulid” key (or vice versa).

4) Standardize identifier domains instead of ad-hoc strings
- Use shared enums/types for known identifier sets (e.g., `ClientName`) rather than free-form strings.

5) Make exported API names disambiguate behavior
- If multiple public functions can be chosen, names must strongly indicate when to use each; ideally export a single “default” function.
- Add comments only after the name makes the choice obvious.

6) Avoid jargon or document it at the source
- If you must use terms like “pointer/dangling/save,” either rewrite to conventional words or add file/function-level explanations of the exact meaning.

7) Treat stable IDs as part of naming correctness
- Identifiers used to target UI/state (e.g., row ids for highlight/skip/undo) must remain stable for the intended lifecycle; encode that lifecycle in the id strategy and document it.