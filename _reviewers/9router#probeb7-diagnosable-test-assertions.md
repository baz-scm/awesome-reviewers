---
title: Diagnosable test assertions
description: 'Write tests so that failures immediately point to the real problem instead
  of producing cryptic, misleading errors.


  - Prefer matcher-based assertions over manual destructuring of mock results. Destructuring
  `vi.mocked(fetch).mock.calls[0]` and then calling `.toBe()` on a piece of it means
  that if the mock was never called, you get an unhelpful `TypeError:...'
repository: decolua/9router#probeB7
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31737
---

Write tests so that failures immediately point to the real problem instead of producing cryptic, misleading errors.

- Prefer matcher-based assertions over manual destructuring of mock results. Destructuring `vi.mocked(fetch).mock.calls[0]` and then calling `.toBe()` on a piece of it means that if the mock was never called, you get an unhelpful `TypeError: undefined is not iterable` instead of a clear test failure. Use `expect(fetch).toHaveBeenCalledWith(expectedUrl, expectedInit)` instead, which reports exactly what was expected vs. what was received (or that the mock was never called at all).

```js
// Avoid
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://localhost:11434/v1/embeddings");

// Prefer
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) })
);
```

- Load shared fixtures, registry entries, or other dynamic/async dependencies inside a `beforeEach`/`before` hook rather than inline at the top of a test or describe block. If the load fails, it should surface as a single, clearly attributed failure rather than cascading into `undefined` errors across unrelated assertions later in the suite.

- When an assertion relies on a non-obvious transformation (e.g., a fixed buffer added to token counts, or other business-logic adjustments), add a short comment at the assertion explaining where the expected value comes from. This prevents future readers from mistaking the value for a typo or bug.

Applying these practices makes test failures self-explanatory, reduces debugging time, and keeps the signal-to-noise ratio of CI failures high.