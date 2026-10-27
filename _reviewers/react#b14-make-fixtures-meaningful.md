---
title: Make Fixtures Meaningful
description: Ensure test fixtures that are evaluated (via `FIXTURE_ENTRYPOINT`) are
  both runnable and capable of catching the regression they’re meant to guard against.
repository: facebook/react#b14
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251893
---

Ensure test fixtures that are evaluated (via `FIXTURE_ENTRYPOINT`) are both runnable and capable of catching the regression they’re meant to guard against.

Apply this when authoring/updating `*.expect.md` fixtures:
1) Runtime must be runnable: if the fixture will be executed, define every referenced symbol (e.g., placeholder components used in the rendered output).
2) Configuration must not dilute coverage: if a fixture’s configuration (like `outputMode`) changes, confirm it still exercises the same validation path and would fail if the target validator/regression behavior changes.

Example (runnable fixture dependency):
```js
// @validateNoDerivedComputationsInEffects
import { useEffect, useState } from 'react';

function MockComponent({ setter }) {
  // minimal runtime implementation so the fixture can evaluate
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

Before merging: (a) run/evaluate the fixture to confirm no missing-runtime-symbol failures, and (b) verify the fixture’s config still triggers the validation behavior it claims to test.