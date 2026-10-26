---
title: Semantic Naming Consistency
description: 'Use names that clearly encode intent, match existing shared identifiers/schemas,
  and stay consistent with the value/type being transported.


  **Rules**'
repository: cline/cline#v18
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70884
---

Use names that clearly encode intent, match existing shared identifiers/schemas, and stay consistent with the value/type being transported.

**Rules**
1) **Prefer shared canonical types/names**: if the codebase has a canonical identifier list/type, use it rather than creating near-duplicates.
2) **Avoid vague booleans**: don’t name flags so that usage requires `!flag` or unclear interpretation. If the domain isn’t truly boolean, model it with a descriptive positive name and an enum-like string union.
3) **Ensure property/event keys match the value’s meaning everywhere**: when renaming telemetry or event properties, update call sites so the identifier format and the property key stay aligned. Positional args can compile even when semantics are wrong.
4) **Apply casing rules predictably by source** (when such a rule exists): e.g., caller-supplied `context` keys use camelCase, while telemetry envelope/global-enrichment keys use snake_case.
5) **Avoid jargon/ambiguous terminology**: choose conventional words; if special terms are required, document what they mean and the correct way to call/use the functions.

**Examples**
- Replace vague boolean intent:
  ```ts
  async function load(refresh: boolean, background = false) {
    // Instead of background/!background, name the intent positively.
  }
  // Better: userInitiated: boolean
  ```
- Replace boolean state with explicit enum-like meaning:
  ```ts
  type RunEntry = "run" | "continue";
  type PromptSeeding = "seeded" | "written";
  ```
- Telemetry rename safety: keep `ulid` values under an `ulid` property key across *all* call sites (or keep the property name as `taskId` if that’s the identifier being reported).