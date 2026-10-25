---
title: Semantic Naming Standards
description: "Adopt naming rules that make intent, ownership, and contracts obvious.\n\
  \n- Use positive, descriptive state names instead of vague booleans.\n  - Prefer\
  \ enums/string unions over `flag: boolean` when the meaning is “seeded vs written\
  \ vs …”."
repository: ClInE/cLiNe
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70838
---

Adopt naming rules that make intent, ownership, and contracts obvious.

- Use positive, descriptive state names instead of vague booleans.
  - Prefer enums/string unions over `flag: boolean` when the meaning is “seeded vs written vs …”.
  - Rename parameters to reflect intent (e.g., `userInitiated` vs `background`).

  ```ts
  type Entry = "run" | "continue";
  type EntryContext = { entry?: Entry; promptSeeded?: boolean /* or replace with positive state */ };
  ```

- Encode “who created the field” in naming/casing when systems mix sources.
  - Example rule: keys supplied by the caller in a `context` object use `camelCase`; keys added by the telemetry envelope/global enrichment use `snake_case`.

- For public helpers, make the right function hard to mis-pick.
  - If two exported functions can be confused, prefer a single obvious “most common” export.
  - Otherwise, rename so the call-site choice is self-evident (and back it with docs).

- Avoid internal jargon names; if you must use domain terms, document them.
  - Names like “dangling pointer” should either be replaced with conventional wording or explained with a clear “what it means / why it exists / how to call it correctly”.

- Treat externally consumed names/keys (telemetry event properties, schema field names, IDs) as contracts.
  - When renaming properties/parameters (e.g., `taskId` → `ulid`), update all call sites and verify event-schema joins. Positional arguments can compile while still sending the wrong semantic identifier.