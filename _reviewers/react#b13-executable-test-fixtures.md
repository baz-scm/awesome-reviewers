---
title: Executable Test Fixtures
description: 'When a fixture exports `FIXTURE_ENTRYPOINT`, treat it as a runtime-evaluated
  test: the code must be executable and the fixture must still trigger the specific
  validation the test intends to cover.'
repository: facebook/react#b13
label: Testing
language: Markdown
comments_count: 3
repository_stars: 251893
---

When a fixture exports `FIXTURE_ENTRYPOINT`, treat it as a runtime-evaluated test: the code must be executable and the fixture must still trigger the specific validation the test intends to cover.

Apply this checklist:
- **Provide runtime definitions for anything referenced during evaluation** (e.g., JSX components, helper functions).
  - Avoid `declare` for functions/values that will be called—implement them.
  - Define mocks used by the fixture (e.g., `MockComponent`).
- **Don’t weaken validation coverage via configuration** (e.g., `outputMode`). If a change makes the fixture no longer exercise the condition under test, the test may stop catching regressions.

Example (runtime-safe fixture):
```js
// @validateNoDerivedComputationsInEffects
import {useEffect, useState} from 'react';

function MockComponent({setter}) {
  return null;
}

function Component({propValue}) {
  const [value, setValue] = useState(null);
  useEffect(() => {
    setValue(propValue);
  }, [propValue]);
  return <MockComponent setter={setValue} />;
}

export const FIXTURE_ENTRYPOINT = {
  fn: Component,
  params: [{ propValue: 'test' }],
};
```

If you change fixture options (like `outputMode`), verify that the fixture still fails/flags under the validation you’re targeting when that validation behavior changes.