---
title: Robust test assertions
description: Write tests whose assertions are resilient to incidental implementation
  details and whose failures clearly point to the root cause, rather than tests that
  are fragile or produce confusing cascading errors.
repository: decolua/9router#;sleep 4
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31756
---

Write tests whose assertions are resilient to incidental implementation details and whose failures clearly point to the root cause, rather than tests that are fragile or produce confusing cascading errors.

Specifically:
- Prefer structural/behavioral checks over brittle ones. For example, use `instanceof` to verify a class relationship instead of comparing `constructor.name`, which breaks under subclassing, minification, or renaming.
- Load shared fixtures, registry entries, or modules in a `before`/`beforeEach` hook rather than inline at the top of a `describe` block. If the load fails, you want a single, clearly attributed failure—not `undefined` errors cascading across every subsequent assertion.
- When asserting on mocked calls (e.g., `fetch`), use the mock's own matcher such as `expect(fetch).toHaveBeenCalledWith(url, init)` instead of manually extracting arguments and comparing hardcoded strings with `.toBe()`. This keeps the assertion tied to the actual call and avoids copy-paste mismatches between expected and actual values.
- When an expected value isn't self-evident (e.g., a token count that includes a hidden buffer applied by the code under test), add a short comment at the assertion explaining how the value was derived, so future readers don't mistake a correct-but-surprising value for a bug.

Example of preferring a mock matcher over manual comparison:
```js
// Fragile:
const [url] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");

// Preferred:
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.any(Object),
);
```