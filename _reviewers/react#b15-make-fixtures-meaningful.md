---
title: Make Fixtures Meaningful
description: 'Tests built from compiler/transform fixtures should be set up so they
  actually exercise the validation they claim to test.


  Apply this when writing/updating fixture `.expect.md` files:'
repository: facebook/react#b15
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251891
---

Tests built from compiler/transform fixtures should be set up so they actually exercise the validation they claim to test.

Apply this when writing/updating fixture `.expect.md` files:

- **Ensure runtime executability:** If a fixture exports `FIXTURE_ENTRYPOINT`, the test runner will evaluate it. Define every referenced component/symbol so failures aren’t caused by missing mocks.

  ```js
  // fixture input
  // ...
  export const FIXTURE_ENTRYPOINT = {
    fn: Component,
    params: [{ propValue: 'test' }],
  };

  // in-file (or included) mock used by evaluation
  function MockComponent({ setter }) {
    return null;
  }
  ```

- **Ensure the harness triggers the intended check:** Don’t add harness config (like `outputMode`) without purpose, but also don’t omit it if omission means the code path that would trigger the error never runs (leading to a test that “passes” without truly validating anything).

  - If the fixture only compiles but the goal is to verify a specific validation diagnostic, confirm the harness settings cause that diagnostic/validation to run; otherwise the test won’t catch regressions.
