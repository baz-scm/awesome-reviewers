---
title: Runnable, Effective Fixtures
description: 'Ensure fixture-based tests both (a) can actually run/evaluate and (b)
  exercise the specific validation/error path the test is meant to cover.


  Apply these rules when adding/updating compiler/test fixtures:'
repository: facebook/react#b3
label: Testing
language: Markdown
comments_count: 2
repository_stars: 251883
---

Ensure fixture-based tests both (a) can actually run/evaluate and (b) exercise the specific validation/error path the test is meant to cover.

Apply these rules when adding/updating compiler/test fixtures:
1) Make the fixture runnable
- If the fixture exports `FIXTURE_ENTRYPOINT`, the runner will evaluate it. Define any referenced components/mocks inside the fixture/module so failures aren’t caused by missing symbols.

```javascript
// Input fixture
// ...
function Component() {
  return <MockComponent />;
}

function MockComponent() {
  return null;
}

export const FIXTURE_ENTRYPOINT = { fn: Component, params: [] };
```

2) Make the fixture effective
- If a fixture must validate a specific rule (e.g., a “no derived computations in effects” / “no setState in effects” lint/diagnostic), configure the fixture’s output mode/flags so the test triggers that pathway. Don’t assume “it compiles” is sufficient—if the intended validation wouldn’t run, the test won’t detect regressions.

Checklist (quick):
- The test would fail for the expected reason if the corresponding validation rule regresses.
- The evaluated entrypoint doesn’t fail early due to missing mocks/symbols.