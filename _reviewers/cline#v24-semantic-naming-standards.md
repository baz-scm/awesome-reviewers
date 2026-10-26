---
title: Semantic Naming Standards
description: 'When naming parameters/properties/IDs, ensure the name communicates
  the *actual domain meaning* and (when relevant) the *provenance* of the value.


  Rules:'
repository: cline/cline#v24
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70891
---

When naming parameters/properties/IDs, ensure the name communicates the *actual domain meaning* and (when relevant) the *provenance* of the value.

Rules:
1) Avoid vague booleans.
   - Prefer names that state the domain intent, or replace boolean flags with positive states (string/enum) that describe what happened.
   - Example: rename a vague `background` flag to `userInitiated` and check `if (userInitiated) { ... }`.

2) Keep name/value meaning consistent across boundaries.
   - If you rename a telemetry property or identifier (e.g., `taskId` → `ulid`), you must also update all call sites and/or types so the emitted property always carries the same identifier format.
   - Don’t rely on positional parameters when the meaning can drift silently.

3) Follow established casing/taxonomy rules that encode provenance.
   - If your codebase convention is “caller-provided `context` keys are camelCase” and “telemetry/envelope enrichment keys are snake_case”, apply that consistently so readers can infer origin.

4) Ensure state/phase names match semantics.
   - Phase names should not invite incorrect interpretation (e.g., “retried” should mean “the retry ran”, not “the run succeeded”).

5) Standardize identifier naming across modules.
   - Align type names and client identifiers with shared conventions (e.g., use the existing `ClientName` vocabulary) to reduce guesswork.

Practical checklist before merging:
- Does the identifier encode intent (not just a boolean)?
- Does the emitted property name match the value’s format at every call site?
- Is casing/provenance consistent with established telemetry/context rules?
- Does the state name accurately describe what is and isn’t being claimed?