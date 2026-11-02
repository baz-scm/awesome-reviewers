---
title: Write robust, self-explanatory assertions
description: 'Test assertions should verify actual behavior and fail with clear, actionable
  diagnostics rather than brittle checks or confusing errors.


  - Prefer semantic/behavioral checks over fragile implementation details. For example,
  assert `instanceof BaseClass` instead of `obj.constructor.name === "SubClass"`,
  since the latter breaks under minification,...'
repository: decolua/9router#zz1793619710
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 31855
---

Test assertions should verify actual behavior and fail with clear, actionable diagnostics rather than brittle checks or confusing errors.

- Prefer semantic/behavioral checks over fragile implementation details. For example, assert `instanceof BaseClass` instead of `obj.constructor.name === "SubClass"`, since the latter breaks under minification, subclassing, or renaming.
- Use the testing framework's built-in matchers for mocks instead of manually destructuring call arguments. For example, prefer:
  ```js
  expect(fetch).toHaveBeenCalledWith(expectedUrl, expectedInit);
  ```
  instead of:
  ```js
  const [url, init] = vi.mocked(fetch).mock.calls[0]; // throws "undefined is not iterable" if fetch was never called
  ```
  This ensures a failed assertion produces a clear message about what was expected vs. actual, rather than an unrelated TypeError when the mock wasn't called as expected.
- When an expected value is derived or non-obvious (e.g., includes buffers, offsets, or transformations applied by the code under test), add a short comment next to the assertion explaining how the value was computed, so future readers don't have to reverse-engineer it.

These practices make test failures easy to diagnose and reduce the maintenance burden of flaky or confusing tests.