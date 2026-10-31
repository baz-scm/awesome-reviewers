---
title: Robust test assertions
description: 'Write assertions that fail with clear, diagnosable messages and that
  stay robust as implementation details change.


  - When asserting on a mocked function''s call arguments, prefer `expect(fn).toHaveBeenCalledWith(...)`
  over manually destructuring from `fn.mock.calls[0]` and comparing with `.toBe()`.
  If the mock was never called, destructuring `undefined`...'
repository: decolua/9router#$(id -u)
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31730
---

Write assertions that fail with clear, diagnosable messages and that stay robust as implementation details change.

- When asserting on a mocked function's call arguments, prefer `expect(fn).toHaveBeenCalledWith(...)` over manually destructuring from `fn.mock.calls[0]` and comparing with `.toBe()`. If the mock was never called, destructuring `undefined` throws an opaque "is not iterable" TypeError instead of a readable assertion failure.

Bad:
```js
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");
```

Good:
```js
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```

- Prefer behavior-based checks over implementation-coupled ones. For example, check `instanceof` to validate class/prototype relationships instead of `instance.constructor.name`, since the latter breaks under minification, renaming, or subclassing.

- When an expected value isn't self-evident (e.g., derived from a buffer, offset, or transformation applied elsewhere in the code), add a short comment at the assertion explaining how the value was derived, so future readers/debuggers don't have to re-trace the logic.

Applying these practices keeps test failures actionable and prevents tests from becoming brittle or cryptic as the codebase evolves.