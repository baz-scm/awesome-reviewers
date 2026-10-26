---
title: Meaningful Runnable Fixtures
description: Test fixtures—especially those evaluated via a `FIXTURE_ENTRYPOINT`—must
  be self-contained and must actually exercise the validation logic they’re meant
  to cover.
repository: facebook/react#b2
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251882
---

Test fixtures—especially those evaluated via a `FIXTURE_ENTRYPOINT`—must be self-contained and must actually exercise the validation logic they’re meant to cover.

Apply this checklist:
1. **Ensure runtime dependencies exist**: If your fixture exports `FIXTURE_ENTRYPOINT` and the test runner evaluates the component, define any referenced components/mocks (and required imports) so failures reflect the targeted validation, not a missing symbol.
2. **Justify harness/output changes (e.g., `outputMode`)**: If a fixture currently compiles, adding `@outputMode:"lint"` (or similar) should be done only when it causes the test to run the rule/paths that would otherwise be missed. Otherwise, the test may no longer catch regressions.

Example (self-contained fixture with required mock):
```js
// @validateNoDerivedComputationsInEffects
import { useEffect, useState } from "react";

function MockComponent({ setter }) {
  // optionally call setter here if you need execution coverage
  return null;
}

function Component({ propValue }) {
  const [, setValue] = useState(null);
  useEffect(() => {
    setValue(propValue);
  }, [propValue]);

  return <MockComponent setter={setValue} />;
}

export const FIXTURE_ENTRYPOINT = {
  fn: Component,
  params: [{ propValue: "test" }],
};
```

When you change test configuration (like `outputMode`), also confirm the fixture still drives the behavior that should trigger the rule under test—otherwise you’ll get “green” tests that aren’t actually validating anything.