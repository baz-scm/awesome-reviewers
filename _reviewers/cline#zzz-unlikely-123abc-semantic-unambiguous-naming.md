---
title: Semantic, unambiguous naming
description: 'Names and types should describe the actual domain, not just encode a
  convenient bit or duplicate an existing concept under a new name.


  1. Prefer descriptive string literal unions (enums) over boolean flags whenever
  the underlying state isn''t truly binary, or when a boolean''s "false" case doesn''t
  describe itself. A positive name for each state is clearer...'
repository: cline/cline#zzz-unlikely-123abc
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 71035
---

Names and types should describe the actual domain, not just encode a convenient bit or duplicate an existing concept under a new name.

1. Prefer descriptive string literal unions (enums) over boolean flags whenever the underlying state isn't truly binary, or when a boolean's "false" case doesn't describe itself. A positive name for each state is clearer than a flag plus its negation. For example, instead of:
```ts
promptSeeded?: boolean; // what does "false" mean here?
```
prefer:
```ts
promptSource?: "seeded" | "written"; // each state is named explicitly
```

2. Before introducing a new type/enum for a concept that already has a name elsewhere in the codebase (e.g. client identifiers, provider ids), reuse or extend the existing type rather than creating a parallel one. Divergent names for the same concept (`ClinePrivacySettingsClient` vs. `ClientName`) create drift and confusion about which is canonical.

3. When exposing multiple public functions/types that address overlapping concerns (e.g. two similarly-named provider-resolution functions), either consolidate into a single public entry point with internal helpers, or give each a name that makes its distinct purpose and precedence obvious, backed by clear doc comments. Don't rely on subtle naming differences (`findUsableFallbackProviderId` vs `resolveEffectiveLastUsedProviderId`) to communicate which one callers should use.

Applying these checks during review prevents ambiguous booleans, duplicate type definitions, and confusingly similar public APIs from accumulating in the codebase.