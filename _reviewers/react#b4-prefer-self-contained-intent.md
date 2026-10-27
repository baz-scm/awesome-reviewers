---
title: Prefer self-contained intent
description: 'When exporting config objects or defining helper APIs, structure code
  so behavior is self-contained and intent is obvious.


  - Prefer `get` accessors (or similarly self-contained constructs) over “declare
  with an empty object, then mutate/reassign later” patterns—this keeps the exported
  shape coherent.'
repository: facebook/react#b4
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251885
---

When exporting config objects or defining helper APIs, structure code so behavior is self-contained and intent is obvious.

- Prefer `get` accessors (or similarly self-contained constructs) over “declare with an empty object, then mutate/reassign later” patterns—this keeps the exported shape coherent.
- Don’t expose implementation-specific types in exported type aliases; use them only for internal validation (e.g., `satisfies`) and keep the public surface clean.
- For helper functions, make data flow explicit: either return the computed result (then merge at the caller) or, if mutating an input collection, make it unmistakable in the signature/naming that the function writes into that argument.

Example pattern (self-contained export via getter):
```ts
const plugin = { /* ... */ };

const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'(): ESLint.Plugin {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};

// Keep public types free of implementation-specific details
type PublicConfig = typeof configs;
```