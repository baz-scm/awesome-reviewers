---
title: Self-contained config initialization
description: 'Prefer code that makes data flow and initialization clear.


  - Avoid “placeholder then reassign/mutate later” patterns for exported configuration
  objects. Build the final shape in a single expression, or use accessors to keep
  construction self-contained.'
repository: facebook/react#b9
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 251891
---

Prefer code that makes data flow and initialization clear.

- Avoid “placeholder then reassign/mutate later” patterns for exported configuration objects. Build the final shape in a single expression, or use accessors to keep construction self-contained.

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

- Keep exported/public types minimal: rely on framework-specific types only for internal `satisfies`/checks, not as part of the exported API surface.
- Prefer minimal function signatures: if the input already has access to needed context, don’t pass the context again.
- Be explicit about mutation vs return: either return the data to be merged by the caller, or clearly design the helper to write into the provided container.