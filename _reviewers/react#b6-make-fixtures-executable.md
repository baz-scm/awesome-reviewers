---
title: Make Fixtures Executable
description: When writing fixture-based tests, ensure they (1) actually execute/run
  in the harness without missing dependencies, and (2) aren’t configured in a way
  that would hide the validation you intend to catch.
repository: facebook/react#b6
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251888
---

When writing fixture-based tests, ensure they (1) actually execute/run in the harness without missing dependencies, and (2) aren’t configured in a way that would hide the validation you intend to catch.

Apply these rules:
- Runtime completeness: If your fixture exports `FIXTURE_ENTRYPOINT` and the runner evaluates the component, define any referenced components/mocks so evaluation can succeed.
- Validation signal preservation: Don’t change harness/compile options (e.g., `outputMode`) unless the fixture truly requires it. If the original fixture already surfaces/guards the validation, avoid configuration that could prevent the expected error from being observed during future changes.

Example (runnable fixture):
```javascript
// @validateNoDerivedComputationsInEffects
import {useEffect, useState} from 'react';

function MockComponent({setter}) {
  // minimal runnable stub
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