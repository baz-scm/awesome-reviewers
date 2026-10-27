---
title: Executable Fixture Tests
description: When adding/changing compiler test fixtures, ensure the fixture is truly
  runnable by the test harness and that it would fail if the intended validation regresses.
repository: facebook/react#b10
label: Testing
language: Markdown
comments_count: 3
repository_stars: 251894
---

When adding/changing compiler test fixtures, ensure the fixture is truly runnable by the test harness and that it would fail if the intended validation regresses.

Apply:
1) Provide runtime definitions for everything the evaluated output references.
- If the compiled/evaluated code expects `MockComponent`, define it in the fixture module (not just in types/assumptions).
- If logic calls helpers like `id`, define them as real functions, not `declare`-only type signatures.

2) If you change fixture harness behavior/config (e.g., `outputMode`), do it only to make the test actually exercise the validation path—so it can catch regressions rather than only “compile successfully”.

Example (runtime definitions):
```javascript
// Avoid: `declare function id<T>(x: T): T;` when the test is evaluated at runtime.
function id(x) {
  return x;
}

function MockComponent({ setter }) {
  return null;
}

export const FIXTURE_ENTRYPOINT = {
  fn: function Component({ propValue }) {
    const [value, setValue] = require('react').useState(null);
    require('react').useEffect(() => setValue(propValue), [propValue]);
    return MockComponent({ setter: setValue });
  },
  params: [{ propValue: 'test' }],
};
```

Checklist:
- Does the fixture module export `FIXTURE_ENTRYPOINT` that the harness will execute?
- Are all referenced identifiers (components, helper functions) defined as runtime values?
- Are any harness/config changes justified by making the test path fail on regressions?