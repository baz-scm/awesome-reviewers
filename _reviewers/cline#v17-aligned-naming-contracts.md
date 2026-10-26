---
title: Aligned Naming Contracts
description: Define and enforce a single canonical naming contract for identifiers/field
  names that represent the same concept across products/variants, and treat any drift
  as a defect.
repository: cline/cline#v17
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70883
---

Define and enforce a single canonical naming contract for identifiers/field names that represent the same concept across products/variants, and treat any drift as a defect.

Apply this standard:
- **Create a canonical schema** (e.g., event JSON fields, configuration keys, option names). Use the same field/identifier names everywhere the concept appears.
- **When renaming, deprecate intentionally**: keep old names temporarily via a compatibility mapping, but clearly mark them deprecated and route to the canonical names.
- **Track mismatches as bugs**: for every discovered case where two products disagree on field/identifier names, open an issue and link it to the schema contract.
- **Avoid silent variant drift**: if variants truly differ, ensure the naming is deterministic and documented; otherwise, align to the same contract.

Example (compatibility mapping for renamed JSON fields):
```ts
type HookInputV1 = { context?: string; contextModification?: string };
type HookInputCanonical = { contextModification?: string };

function normalizeHookInput(input: HookInputV1): HookInputCanonical {
  // v1 old name -> canonical
  const { context, contextModification, ...rest } = input;
  if (contextModification == null && context != null) {
    console.warn('[deprecation] "context" is deprecated; use "contextModification"');
    return { ...rest, contextModification: context };
  }
  return { ...rest, contextModification };
}
```

Result: code remains easier to reason about, docs reflect one truth, and users aren’t surprised by identifier/field-name differences between product builds.