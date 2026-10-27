---
title: Executable, Meaningful Fixtures
description: When writing compiler/test fixtures that export a `FIXTURE_ENTRYPOINT`,
  ensure the fixture is both (1) runnable/evaluable and (2) configured to actually
  exercise the validation/behavior the test is intended to catch.
repository: facebook/react#b17
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251891
---

When writing compiler/test fixtures that export a `FIXTURE_ENTRYPOINT`, ensure the fixture is both (1) runnable/evaluable and (2) configured to actually exercise the validation/behavior the test is intended to catch.

- **Run-time dependencies must exist**: If the evaluated output references components/helpers (e.g., `MockComponent`), define them in the fixture so the test can execute.
- **Test configuration must enable the check**: If you change settings like `outputMode` to trigger a specific lint/validation, don’t set them blindly—but also don’t leave them out if the fixture otherwise wouldn’t exercise the rule (otherwise the test may compile and never detect the intended error).

Example (runnable fixture with required mock):
```js
// @validateNoDerivedComputationsInEffects
import { useEffect, useState } from 'react';

function MockComponent({ setter }) {
  return null;
}

function Component({ propValue }) {
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

Apply the same mindset to configuration: only adjust options (like `outputMode`) when necessary to ensure the test actually runs the intended validation path.