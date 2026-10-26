---
title: Executable Fixture Discipline
description: When writing/adjusting fixture-based tests, assume the test runner will
  execute the fixture’s exported entrypoint. Make the fixture both (a) runnable at
  runtime and (b) configured to emit the validation signal you’re trying to catch—so
  regressions can’t be silently missed.
repository: facebook/react#b1
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251878
---

When writing/adjusting fixture-based tests, assume the test runner will execute the fixture’s exported entrypoint. Make the fixture both (a) runnable at runtime and (b) configured to emit the validation signal you’re trying to catch—so regressions can’t be silently missed.

Apply this checklist:
- Runtime dependencies: If `FIXTURE_ENTRYPOINT.fn` (or generated code) references components/mocks/helpers, define them in the fixture input so evaluation doesn’t fail early.
- Explicit validation configuration: Don’t rely on implicit/default fixture directives when they could prevent the specific validation from producing output (e.g., lint vs compile-only). Set the directive explicitly when needed so the test fails if the underlying validation rule changes.

Example (ensure fixture is runnable by defining mocks):
```js
// @validateNoDerivedComputationsInEffects
import { useEffect, useState } from 'react';

function MockComponent() {
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

Outcome: fixtures that either execute successfully up to the validation-relevant portion and/or fail for the right reasons, making the test suite reliable against future regressions.