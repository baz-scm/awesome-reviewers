---
title: Make Intent Explicit
description: 'When shaping objects/configs or collecting data, prefer patterns that
  are self-contained and make intent/data flow obvious.


  - Avoid “placeholder then reassign/mutate later” structures when a direct/self-contained
  construction is clearer. If your export needs computed properties, prefer accessors/getters.'
repository: facebook/react#b6
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251888
---

When shaping objects/configs or collecting data, prefer patterns that are self-contained and make intent/data flow obvious.

- Avoid “placeholder then reassign/mutate later” structures when a direct/self-contained construction is clearer. If your export needs computed properties, prefer accessors/getters.

Example (getter-based config instead of placeholder reassignment):
```ts
const plugin = { /* ... */ };

export const configs = {
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

- For functions that populate external state (e.g., a `Set` passed in), make it obvious you’re writing to that argument. Either:
  1) Return the collected values and let the caller merge, or
  2) Keep the side effect but structure/naming so it’s clear (and consider returning `void` explicitly).

Rule of thumb: if a reader has to infer whether code is constructing vs later swapping vs mutating inputs, refactor so the choice is explicit in the shape of the code.