---
title: Prefer semantic naming
description: 'Use names that make intent and correct usage obvious.


  Rules:

  - **Encode domain meaning, not convenience flags.** If a field is really a state
  (“seeded vs written”), don’t use a boolean that forces readers to infer negation—use
  a string/enum.'
repository: cline/cline#v2
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70861
---

Use names that make intent and correct usage obvious.

Rules:
- **Encode domain meaning, not convenience flags.** If a field is really a state (“seeded vs written”), don’t use a boolean that forces readers to infer negation—use a string/enum.
  ```ts
  // Prefer
  entry?: "run" | "continue"; // seeded vs written style
  promptSeeded?: boolean; // -> replace with a positive state if domain is multi-valued
  ```
- **Name boolean parameters/fields by intent.** Replace vague flags like `background` with what the caller means (e.g. `userInitiated`), and ensure the name matches mount/initial behavior.
  ```ts
  async function load(userInitiated: boolean, /*...*/)
  ```
- **Make identity/lifecycle stable in naming.** If actions reference “a row” or “a turn”, ensure the id naming/semantics remain consistent across updates so consumers don’t need hidden rules.
- **Design exported APIs so the right choice is obvious.** Avoid “two similar exported functions where it’s unclear which one to call”; either export one canonical entry point or use names that clearly distinguish responsibility.
- **Follow existing naming/casing conventions by provenance.** Example: telemetry keys added by the caller vs added by the telemetry envelope should keep the established casing split (e.g., caller-supplied context keys camelCase; envelope/global enrichment keys snake_case).

Checklist to apply in review:
- Can a developer tell *what this parameter/state means* without reading the implementation?
- Can a developer tell *which exported function to call* from the names alone?
- Are naming/casing conventions preserved for the key’s provenance (caller vs framework)?
- For identity-like values (ids, revisions), does the naming/semantics stay stable for the duration the UI/actions assume?