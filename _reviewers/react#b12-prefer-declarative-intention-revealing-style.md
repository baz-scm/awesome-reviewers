---
title: Prefer declarative, intention-revealing style
description: 'When defining exports/configs or helper APIs, prefer patterns that are
  declarative and make intent obvious.


  - Avoid “placeholder then patch” object construction. Build the final shape in one
  pass rather than assigning an empty object and later reassigning/mutating it.'
repository: facebook/react#b12
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251896
---

When defining exports/configs or helper APIs, prefer patterns that are declarative and make intent obvious.

- Avoid “placeholder then patch” object construction. Build the final shape in one pass rather than assigning an empty object and later reassigning/mutating it.
- For lazy/dynamic values inside exported objects, use getters to keep the definition self-contained and scoped.
- Keep exported/public types decoupled from framework-specific types; use `satisfies` for validation rather than baking those types into exported signatures.
- For helpers, avoid unclear side effects: either return computed data for the caller to merge, or make the mutation intent explicit in the signature/name.

Example (getter-based, self-contained config):
```ts
const plugin = {/* ... */};

export const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
} satisfies {/* expected config shape */};
```

Example (prefer returning vs mutating):
```ts
function getFnGlobalDeps(fn: FunctionExpression | undefined): IdentifierId[] {
  if (!fn) return [];
  // compute deps...
}

// caller merges
const deps = new Set(getFnGlobalDeps(fn));
```