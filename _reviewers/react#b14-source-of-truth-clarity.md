---
title: Source-of-truth Clarity
description: 'When implementing logic or metadata, ensure it’s driven by the correct
  single source of truth and expressed declaratively.


  Apply this standard:

  - Prefer using capabilities already available on the primary object (e.g., IR/HIR)
  instead of threading extra parameters just to re-access context.'
repository: facebook/react#b14
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 251893
---

When implementing logic or metadata, ensure it’s driven by the correct single source of truth and expressed declaratively.

Apply this standard:
- Prefer using capabilities already available on the primary object (e.g., IR/HIR) instead of threading extra parameters just to re-access context.
- Avoid redundant type/guard checks when dataflow (or the real dependency analysis) already determines the outcome. Don’t mix “dataflow + typing” gating unless both are truly required.
- Model semantic metadata precisely: argument-by-argument effect/permission behavior should match actual runtime behavior (reads vs stores/captures).
- For config structures, avoid “create empty object, then mutate/replace” patterns; prefer self-contained declarations (e.g., getter-based plugin resolution) for readability and locality.

Example pattern (getter-based, self-contained config):
```ts
const plugin = { meta: { name: 'eslint-plugin-react-hooks', version: '7.0.0' }, rules };

const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin; // no placeholder object then reassignment
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```

Example pattern (dataflow-only gating + accurate semantic intent):
- If dataflow already determines “setState usage”, don’t additionally require a type predicate before recording it.
- When annotating effects for a built-in like `fill(value, start, end)`, mark `value` as the captured/stored argument and the rest as reads.

This reduces brittleness, removes unnecessary complexity, and makes future changes safer.