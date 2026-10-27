---
title: Meaningful Runnable Fixtures
description: When using fixture-based tests (e.g., exporting `FIXTURE_ENTRYPOINT`),
  ensure the fixture is both runnable and actually exercises the intended validator.
repository: facebook/react#b11
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251894
---

When using fixture-based tests (e.g., exporting `FIXTURE_ENTRYPOINT`), ensure the fixture is both runnable and actually exercises the intended validator.

- **Self-contained runtime**: If the test runner evaluates the component, define every referenced symbol (mocks/components) inside the fixture module.
- **Don’t accidentally bypass validation**: If you change harness/config (e.g., `@outputMode:"lint"`), confirm it doesn’t prevent the specific check from running—otherwise a validator regression may go unnoticed.

Example (runnable fixture with required mock):
```js
// @validateNoDerivedComputationsInEffects
import { useEffect, useState } from 'react';

function MockComponent({ setter }) {
  // minimal implementation so evaluation doesn’t crash
  setter('ok');
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

Checklist to apply during review:
1) Can the fixture be evaluated end-to-end without `ReferenceError`/missing identifiers?
2) Do harness attributes/config still trigger the targeted validation?
3) Would the fixture fail if the validator behavior regressed (i.e., no “silent pass” due to config)?