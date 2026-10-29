---
title: Test fidelity and assertions
description: 'Tests must exercise the real production code path and fail with clear,
  actionable diagnostics when they break.


  1. Never duplicate implementation logic inside a test file "for isolation." If a
  helper (e.g. `stripReasoningContent`) is only defined and tested as a local copy,
  the test can pass while the real exported function is broken or never even reached....'
repository: Decolua/9Router
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 31641
---

Tests must exercise the real production code path and fail with clear, actionable diagnostics when they break.

1. Never duplicate implementation logic inside a test file "for isolation." If a helper (e.g. `stripReasoningContent`) is only defined and tested as a local copy, the test can pass while the real exported function is broken or never even reached. Export the function/class from the source module and import it directly in the test, so the test proves the production code behaves as expected.

2. Prefer semantic checks over structural ones when verifying class relationships or call behavior. Use `instanceof` instead of `constructor.name` to assert inheritance, and use `expect(mock).toHaveBeenCalledWith(...)` instead of destructuring `mock.calls[0]` or asserting on raw call arguments with `.toBe()`. Destructuring an empty calls array throws an opaque `undefined is not iterable` error that hides the real failure, whereas `toHaveBeenCalledWith` reports exactly what was expected vs. received:

```js
// Avoid: throws unhelpful TypeError if fetch was never called
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://localhost:11434/v1/embeddings");

// Prefer: clear, self-describing failure message
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.stringContaining('"model":"nomic-embed-text"') }),
);
```

3. Load shared fixtures/modules used across multiple test cases (e.g., a dynamically-imported registry entry) in a `before()`/`beforeAll()` hook rather than inline per-test, so a load failure surfaces as one clear failure instead of cascading as confusing `undefined` assertions in every dependent test.

4. When an expected value in an assertion isn't self-evident (e.g., it includes a hidden buffer or transformation applied by the code under test), add a short comment explaining the derivation so future readers don't have to reverse-engineer it.

Applying these practices keeps test suites trustworthy, makes failures self-explanatory, and ensures tests actually validate the shipped implementation rather than a parallel copy of it.