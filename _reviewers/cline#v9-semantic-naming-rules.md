---
title: Semantic Naming Rules
description: When choosing names for identifiers (types, functions, parameters, fields,
  telemetry properties), make them *semantically precise* and *unambiguous about usage
  and origin*.
repository: cline/cline#v9
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70868
---

When choosing names for identifiers (types, functions, parameters, fields, telemetry properties), make them *semantically precise* and *unambiguous about usage and origin*.

Apply these rules:
- Prefer intent-revealing names over vague booleans. If the boolean represents a concept (not “background”), name it as the concept.
  - Example: rename `load(refresh, background)` to `load(refresh, userInitiated)` or `load(refresh, /* userInitiated */)`.
- Avoid boolean fields for domain states where negation isn’t the real meaning. Use descriptive positive states (string unions/enums) instead.
  - Example:
    ```ts
    entry?: "run" | "continue";
    promptState?: "seeded" | "written"; // instead of promptSeeded?: boolean
    ```
- Ensure naming matches identifier semantics everywhere it matters (especially telemetry/schema). If you rename a property from `taskId` to `ulid`, update all call sites and keep the event schema consistent so downstream consumers can reliably join/group by the right identifier.
- Keep structural conventions consistent with value provenance. For telemetry keys, use casing that matches whether keys come from caller-supplied context vs system/global enrichment.
- For exported APIs, avoid multiple similarly-purpose functions with names that make it hard to choose. Prefer one obvious entrypoint, or clearly document/encode which one callers should use.
- Don’t rely on jargon (“pointer/dangling/save”) unless the file/function explains the terms or you choose clearer, conventional wording.

If a developer can’t tell what a name means (or which API to call) without reading implementation details, the naming likely violates this rule.