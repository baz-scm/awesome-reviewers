---
title: Clear, robust test assertions
description: 'Tests should exercise the real implementation and fail with clear, actionable
  messages when something goes wrong.


  - Test the actual exported function/class, not a hand-copied reimplementation of
  its logic. If a test needs to isolate a helper, import and call the real one rather
  than pasting a "mirror" of it into the test file — otherwise the test can pass...'
repository: decolua/9router?x
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31748
---

Tests should exercise the real implementation and fail with clear, actionable messages when something goes wrong.

- Test the actual exported function/class, not a hand-copied reimplementation of its logic. If a test needs to isolate a helper, import and call the real one rather than pasting a "mirror" of it into the test file — otherwise the test can pass while the real code diverges.
- Prefer behavior-based checks over implementation-detail checks, e.g. use `instanceof` / prototype-chain checks instead of comparing `constructor.name` strings when asserting class hierarchy.
- When test setup involves async loading (dynamic imports, fixture loading, etc.), fail fast: load dependencies in a `before`/`beforeAll` hook so a setup failure surfaces as one clear error instead of cascading into confusing `undefined` failures across many later assertions.
- For mock-based assertions, avoid manually destructuring `mock.calls[0]` and comparing with `toBe()`. If the mock was never called, destructuring `undefined` throws an opaque `TypeError` instead of a useful test failure; and plain `toBe()` only gives a generic mismatch. Prefer `expect(mockFn).toHaveBeenCalledWith(...)`, which produces a readable diff and clearly states whether the call happened and with what arguments.
- When an assertion encodes a non-obvious derived value (e.g., a token count inflated by an internal buffer), add a short inline comment explaining how the expected value was derived so future readers don't mistake it for a bug.

Example:
```js
// Avoid:
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe(expectedUrl);

// Prefer:
expect(fetch).toHaveBeenCalledWith(expectedUrl, expect.objectContaining({ body: expectedBody }));
```