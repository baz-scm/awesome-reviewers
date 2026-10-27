---
title: Prefer declarative, precise modeling
description: When creating exported structures/configs or encoding semantic/effect
  models, favor declarative, self-contained code and exact semantics over “define-then-mutate”
  patterns.
repository: facebook/react#b13
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 251893
---

When creating exported structures/configs or encoding semantic/effect models, favor declarative, self-contained code and exact semantics over “define-then-mutate” patterns.

- Avoid initializing an empty container and mutating/reassigning it later; prefer a single, self-contained definition (e.g., using getters) so the exported shape is correct at declaration time.
- Keep helper APIs explicit about intent (if a function writes into a collection, either name/shape it to make that obvious or return values that the caller merges).
- Don’t mix concerns in analysis/validation: if the intended correctness mechanism is dataflow, avoid extra type-based gates that duplicate or obscure the real source of truth.
- Ensure modeled parameter/effect lists match the actual call contract precisely (e.g., `with(index, value)` should reflect `positionalParams: [Effect.Read, Effect.Capture]`).

Example pattern (declarative config via getter):
```ts
export const pluginConfig = {
  recommended: {
    plugins: {
      get 'react-hooks'(): ESLint.Plugin {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```