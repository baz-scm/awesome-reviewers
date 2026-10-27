---
title: API Compatibility and Context
description: 'When designing or changing an API surface (including compiler/plugin
  entrypoints and options):


  1) Don’t pass redundant context through parameters

  - If the callee can access the needed environment via an owned object (e.g., `hir`
  already has access to `env`), prefer using that internal access over threading extra
  arguments.'
repository: facebook/react#b13
label: API
language: TypeScript
comments_count: 2
repository_stars: 251893
---

When designing or changing an API surface (including compiler/plugin entrypoints and options):

1) Don’t pass redundant context through parameters
- If the callee can access the needed environment via an owned object (e.g., `hir` already has access to `env`), prefer using that internal access over threading extra arguments.
- This keeps the API smaller and reduces coupling between caller and callee.

Example (preferred pattern):
```ts
// If `hir` can already read its environment internally,
// avoid passing `env` as a separate parameter.
validateExhaustiveDependencies(hir).unwrap();
```

2) Deprecate before removing option/API fields
- Treat options as an API contract even if they are not currently documented.
- Prefer marking as deprecated and keeping behavior compatible for at least one release cycle, then remove later.
- Explicitly consider whether removal would be a breaking change for downstream users relying on that option.

Example (preferred pattern):
```ts
// 1) Keep the option, but mark deprecated in code comments/types.
// 2) Add runtime warnings when used.
// 3) Remove only after a deprecation window.
```

Applied together, these rules reduce unnecessary interface churn (fewer parameters) while also protecting downstream integrations from abrupt option removals.