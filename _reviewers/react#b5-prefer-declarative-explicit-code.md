---
title: Prefer Declarative, Explicit Code
description: 'When defining exported structures or helper utilities, favor patterns
  that make intent and data flow obvious.


  - Avoid placeholder objects followed by later reassignment (e.g., create an empty
  object and then `Object.assign` to fill it). Prefer defining the full structure
  up front. If you need lazy evaluation, use a getter so the object remains...'
repository: facebook/react#b5
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251886
---

When defining exported structures or helper utilities, favor patterns that make intent and data flow obvious.

- Avoid placeholder objects followed by later reassignment (e.g., create an empty object and then `Object.assign` to fill it). Prefer defining the full structure up front. If you need lazy evaluation, use a getter so the object remains self-contained.

  Example (self-contained config via getter):
  ```ts
  const plugin = { meta: { name: 'eslint-plugin-react-hooks', version: '7.0.0' }, rules };

  export const configs = {
    recommended: {
      plugins: {
        get 'react-hooks'(): any {
          return plugin;
        },
      },
      rules: recommendedRuleConfigs,
    },
  };
  ```

- Prefer returning computed values over mutating parameters. If mutating is necessary (e.g., adding entries to a `Set`), make it clearly explicit in naming/signature so it’s obvious the function is producing data via side effects.

  Prefer return + merge:
  ```ts
  function getFnGlobalDeps(fn: FunctionExpression | undefined): Array<IdentifierId> {
    // compute deps...
    return [];
  }

  depsSet = new Set(getFnGlobalDeps(fn));
  ```

  Or, if keeping `deps` mutation, ensure the intent is unmistakable (e.g., name the parameter like `outDeps` / `depsToFill`).