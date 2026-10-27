---
title: Meaningful Runnable Fixtures
description: When writing fixture-based tests, ensure they (1) execute the code paths
  that should trigger the specific validation being tested and (2) are runnable in
  the test harness.
repository: facebook/react#b7
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251888
---

When writing fixture-based tests, ensure they (1) execute the code paths that should trigger the specific validation being tested and (2) are runnable in the test harness.

Apply this by:
- **Make fixtures executable:** If a fixture exports `FIXTURE_ENTRYPOINT` that the runner evaluates, define all required helpers/components/mocks used by the evaluated code.
- **Avoid “no-op” coverage:** Don’t assume an error will be caught if the code that could trigger the validation doesn’t run. If harness options (e.g., `outputMode`) affect whether validations are enforced, set them so the test actually exercises the rule.

Example (runnable fixture with required mock):
```javascript
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

Before committing, quickly sanity-check that the fixture evaluation won’t fail due to missing symbols and that the targeted validation condition is actually reachable/exercised by the fixture inputs and configuration.