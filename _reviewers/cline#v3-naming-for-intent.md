---
title: Naming for Intent
description: 'Use names that clearly encode intent and follow the project’s established
  naming conventions—especially across public APIs and telemetry/events.


  Rules:'
repository: cline/cline#v3
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70863
---

Use names that clearly encode intent and follow the project’s established naming conventions—especially across public APIs and telemetry/events.

Rules:
1. Prefer established shared identifiers/types
   - When a canonical name/type exists (e.g., a shared `ClientName`), align new client-related types to it rather than introducing near-duplicates.

2. Avoid vague boolean flags
   - If a boolean can’t be read as a direct, positive meaning at the call site, rename it to the underlying intent.
   - Where the domain is multi-state, replace booleans with explicit string/enum-like states (prefer positive states over “not X”).
   - Example:
     ```ts
     // Before
     function load(refresh: boolean, background = false) {}

     // After
     function load(refresh: boolean, userInitiated = false) {}
     // or (multi-state)
     type EntryKind = "run" | "continue";
     ```

3. Make exported APIs easy to choose
   - If multiple functions exist, ensure their names strongly indicate when to call each.
   - If there’s a “single right thing” most callers should use, export that as the primary entry point and keep helpers clearly marked (or tucked behind testing/internal namespaces).

4. Renames must update semantics everywhere
   - Property/key renames (e.g., `taskId` → `ulid`) must update all call sites and maintain consistent key meaning across events—downstream integrations often depend on stable identifiers.

5. Follow existing casing rules by identifier origin
   - Don’t invent casing for telemetry keys/events; follow the convention the codebase already uses (e.g., caller-supplied context vs envelope/global-enrichment keys).

Practical checklist for PRs:
- Can a reviewer tell what a boolean means by reading the call site?
- Are names aligned to existing canonical types/patterns?
- Do exported functions have “obvious selection” names (or is one clear primary API missing)?
- If a key/property name changes, were all call sites updated and downstream expectations checked?
- Did you follow the repo’s casing convention for that category/origin of identifier?