---
title: Use intentful, consistent names
description: 'Adopt naming that makes intent, provenance, and selection obvious, and
  that prevents semantic drift.


  Guidelines:

  - Reuse shared naming types for identifiers.'
repository: cline/cline#v15
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70877
---

Adopt naming that makes intent, provenance, and selection obvious, and that prevents semantic drift.

Guidelines:
- Reuse shared naming types for identifiers.
  - If a common `ClientName` (or similar) exists, use it instead of ad-hoc string unions or “escape hatch” strings.
- Avoid vague boolean parameters/fields.
  - If the domain has more than “true/false” meaning, replace booleans with explicit unions/enums that describe the state positively.
  - Example:
    ```ts
    // Prefer:
    entry?: 'run' | 'continue'
    promptState?: 'seeded' | 'written'

    // Over:
    // entry?: boolean
    // promptSeeded?: boolean
    ```
- Ensure public exported functions are easy to choose.
  - Export one “obvious default” when possible; if multiple helpers must be public, name them so a caller can tell which one to call without reading implementation.
- Keep naming conventions consistent by origin/provenance.
  - For mixed key sets (e.g., caller context vs telemetry envelope/global enrichment), follow the established rule for where the key comes from (camelCase for caller-supplied context keys; snake_case for envelope/global keys).
- Prevent semantic drift when renaming properties.
  - Renaming an event property key/meaning (e.g., `taskId` → `ulid`) is not just a rename—update call sites and ensure the property key always carries the same identifier type across all emitters.
- Replace magic values with named constants when they affect behavior and timing.
  - This improves readability and reduces “mystery intent” in event/timeout logic.

When reviewing code, ask:
- “Does the name tell the developer what it means (not just what it is)?”
- “Is this identifier pulled from the shared source of truth?”
- “Are we following the correct naming convention for the key’s origin?”
- “If semantics changed, were all call sites and downstream expectations updated?”