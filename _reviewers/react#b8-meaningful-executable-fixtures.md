---
title: Meaningful Executable Fixtures
description: When writing compiler/fixture-based tests (e.g., files exporting `FIXTURE_ENTRYPOINT`),
  ensure the test is both runnable and actually exercises the validation/behavior
  you intend to guard.
repository: facebook/react#b8
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251889
---

When writing compiler/fixture-based tests (e.g., files exporting `FIXTURE_ENTRYPOINT`), ensure the test is both runnable and actually exercises the validation/behavior you intend to guard.

1) Keep the fixture behavior meaningful
- Don’t add/adjust `outputMode` (or similar knobs) unless it changes whether the test will surface the intended compiler validation.
- Otherwise, the fixture may “compile w/o error” and stop detecting regressions (so changes to the validation rule wouldn’t make the test fail).

2) Make the fixture self-contained
- Any component/mock referenced by the evaluated fixture must be defined within the fixture inputs/exports.

Example (self-contained fixture to avoid runtime failures):
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
  params: [{propValue: 'test'}],
};
```

Checklist before merging fixture changes:
- Would this fixture fail if the relevant validation regressed?
- Does the fixture run end-to-end in the test runner with all referenced mocks/components defined?
- Have changes to compiler flags/output modes been justified by a change in what the fixture asserts?