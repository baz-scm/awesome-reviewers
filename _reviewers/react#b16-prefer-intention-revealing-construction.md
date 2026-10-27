---
title: Prefer intention-revealing construction
description: 'When building exported objects or APIs, prefer patterns that make data
  flow and intent explicit.


  - Avoid “declare as empty → mutate/reassign later” constructions for exported config/state.
  Prefer self-contained definitions (e.g., accessor/getter-based properties) so the
  final shape is clear at the declaration site.'
repository: facebook/react#b16
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When building exported objects or APIs, prefer patterns that make data flow and intent explicit.

- Avoid “declare as empty → mutate/reassign later” constructions for exported config/state. Prefer self-contained definitions (e.g., accessor/getter-based properties) so the final shape is clear at the declaration site.
- Keep exported types free from unnecessary framework-specific types when possible; use those types only for internal `satisfies` checks rather than baking them into exported signatures.
- For functions that communicate results, prefer returning values. If you must mutate an accumulator (e.g., a `Set`), make the intent obvious in the function signature/implementation (or restructure to return data and merge at the caller).

Example (getter-based config to avoid empty-then-reassign):
```ts
const plugin = { /* meta, rules, etc. */ };

const config = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```

If a helper currently accepts `deps: Set<...>` and mutates it, either:
- return the collected identifiers and merge at the caller, or
- rename/structure the code so it’s immediately clear that the function is writing into `deps` (rather than computing an independent result).