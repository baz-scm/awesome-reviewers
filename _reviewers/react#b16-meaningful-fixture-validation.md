---
title: Meaningful Fixture Validation
description: When writing compiler/test fixtures that the runner evaluates (via `FIXTURE_ENTRYPOINT`),
  ensure the fixture is both runnable and actually asserts the intended validation.
repository: facebook/react#b16
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251891
---

When writing compiler/test fixtures that the runner evaluates (via `FIXTURE_ENTRYPOINT`), ensure the fixture is both runnable and actually asserts the intended validation.

- **Keep fixtures self-contained:** if the compiled/evaluated code references mocks/components, define them in the fixture inputs/fixtures so the runner doesn’t fail for unrelated reasons (e.g., `MockComponent is not defined`).
- **Don’t mask coverage with unnecessary test configuration:** only set special options (like `outputMode`) when it’s required for the fixture to exercise the specific validator being tested. Otherwise, you may turn a test into a “compile-only” check that won’t detect regressions (e.g., a validator change that should start erroring).

Example (make the fixture runnable):
```js
// In the same fixture file / test scope
function MockComponent({ setter }) {
  // minimal runnable stub
  return null;
}

export const FIXTURE_ENTRYPOINT = {
  fn: Component,
  params: [{ propValue: 'test' }],
};
```

Example (avoid undermining the assertion):
- If a fixture compiles “fine” already, verify that the added configuration is necessary; if not, remove it so the fixture can fail when the target validation regresses.