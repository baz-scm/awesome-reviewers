---
title: Semantic Naming Standards
description: 'Use names that encode the *actual meaning* and follow the project’s
  *identifier contracts/conventions*.


  - **Avoid vague booleans/flags**: rename to what the value *means*, not what it
  excludes.'
repository: Cline/Cline
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 70840
---

Use names that encode the *actual meaning* and follow the project’s *identifier contracts/conventions*.

- **Avoid vague booleans/flags**: rename to what the value *means*, not what it excludes.
  - Bad: `load(refresh, background)`
  - Good: `load(refresh, userInitiated)`
- **Don’t model domain states as booleans**: if it’s really “seeded vs written vs …”, use a string union/enum (e.g. `entry?: "run" | "continue"`).
- **Keep shared names aligned with shared types/contracts**: if there is a canonical type (e.g. `ClientName`), don’t invent parallel strings.
- **Treat event/telemetry property keys as schema contracts**: renaming `taskId`→`ulid` requires updating *all* call sites and auditing consumers that join on the old key.
- **Name public APIs to reduce ambiguity**: either expose one obvious entry point, or make the names clearly indicate which one to call (and add decisive comments if both must remain public).
- **Apply casing conventions by identifier origin** (when applicable): e.g. caller-supplied `context` keys use `camelCase`, while envelope/global-enrichment keys use `snake_case`.
- **Eliminate magic values**: extract important numeric timings into named constants and document their purpose.

Following these rules prevents “looks-like-it-compiles-but-is-wrong” naming drift and makes identifiers self-explanatory for future call sites.