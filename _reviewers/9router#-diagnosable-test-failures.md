---
title: Diagnosable test failures
description: 'Write tests so that when they fail, the failure message points directly
  to the root cause instead of producing cryptic, cascading errors. This applies to
  assertion style, fixture/setup loading, and documentation of non-obvious expected
  values:'
repository: decolua/9router#
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31729
---

Write tests so that when they fail, the failure message points directly to the root cause instead of producing cryptic, cascading errors. This applies to assertion style, fixture/setup loading, and documentation of non-obvious expected values:

1. Prefer built-in matchers over manual extraction of mock call data. Destructuring `mock.calls[0]` when the mock was never invoked throws an opaque `TypeError: undefined is not iterable`, hiding the real problem. Use the matcher instead:
```js
// Bad: throws a confusing TypeError if fetch was never called
const [url, init] = vi.mocked(fetch).mock.calls[0];

// Good: clear failure message if the call didn't happen as expected
expect(fetch).toHaveBeenCalledWith(expectedUrl, expectedInit);
```

2. Verify contracts with robust checks rather than brittle string comparisons. Use `instanceof` against the base class instead of comparing `constructor.name`, which breaks under minification/bundling and doesn't actually prove the prototype chain:
```js
// Bad
assert.equal(inst.constructor.name, "KimchiExecutor");

// Good
assert.ok(inst instanceof DefaultExecutor);
```

3. Isolate risky setup (dynamic imports, registry lookups, fixture loading) in `before`/`beforeEach` hooks rather than inline in the test body, so a load failure surfaces as one clear failure instead of cascading into multiple confusing "undefined" assertion errors downstream.

4. When an assertion's expected value involves a non-obvious transformation (e.g., a token count that includes a hidden buffer, or similar derived/computed value), add a short comment at the assertion explaining why that value is correct, so future readers don't have to trace through the implementation to understand the test.

Following these practices keeps test failures fast to diagnose and reduces time spent debugging the test itself instead of the actual bug.