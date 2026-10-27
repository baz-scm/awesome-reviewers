---
title: Meaningful Fixture Tests
description: When using fixture-based tests that the runner evaluates, ensure they’re
  (1) runnable/self-contained and (2) configured to actually exercise the intended
  validation/regression.
repository: facebook/react#b12
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251896
---

When using fixture-based tests that the runner evaluates, ensure they’re (1) runnable/self-contained and (2) configured to actually exercise the intended validation/regression.

Apply this rule:
- **Runnability**: If the fixture exports `FIXTURE_ENTRYPOINT`, the test harness will execute/evaluate it. Define any referenced components/functions (mock them as needed) so failures are about the validation under test—not missing symbols.
- **Meaningful assertion**: If a validation rule is meant to be checked (e.g., “no derived computations in effects”), make sure the fixture is configured so the runner/transform will surface that error. If the default configuration would let the fixture pass silently, set the required mode/flags so the test can catch regressions.

Example (self-contained fixture):
```javascript
// @validateNoDerivedComputationsInEffects
import {useEffect, useState} from 'react';

function MockComponent({ setter }) {
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

Checklist for changes to fixture expected outputs:
- Does the fixture include all runtime identifiers it uses?
- Does the fixture configuration ensure the intended validator is actually triggered (not just compiled)?
- Would a regression in the targeted validator change the expected output/exception? If not, the test likely isn’t meaningful yet.