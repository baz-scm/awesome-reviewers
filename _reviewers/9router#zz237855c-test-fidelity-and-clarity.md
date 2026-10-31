---
title: Test fidelity and clarity
description: 'Tests should exercise the real production code path and fail in a way
  that immediately tells you what went wrong.


  1. Import and test the actual implementation rather than re-declaring or copying
  logic into the test file. Duplicated "mirror" helpers drift from the real code and
  give false confidence (e.g., a test defining its own `stripReasoningContent`...'
repository: decolua/9router#zz237855c
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31752
---

Tests should exercise the real production code path and fail in a way that immediately tells you what went wrong.

1. Import and test the actual implementation rather than re-declaring or copying logic into the test file. Duplicated "mirror" helpers drift from the real code and give false confidence (e.g., a test defining its own `stripReasoningContent` instead of importing the exported function from the executor). Similarly, when asserting on class/type relationships, check the real prototype chain (`instanceof`) instead of brittle string checks like `constructor.name`.

2. Load shared fixtures/modules needed by multiple tests in a `before()`/`beforeAll()` hook rather than inline inside an `it()`. If the load fails, you get one clear failure instead of a cascade of confusing `undefined` assertion errors in every subsequent test.

3. Prefer purpose-built mock assertions over manual destructuring and loose equality checks. Instead of:
```js
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");
```
use:
```js
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```
This avoids cryptic `TypeError: undefined is not iterable` when the mock was never called, and produces a readable diff when the actual call doesn't match expectations.

4. When an assertion encodes a non-obvious transformation (e.g., a token count that includes a fixed buffer added by the handler), add a short comment next to the assertion explaining where the number comes from, so future readers don't mistake it for a bug.

Applying these practices keeps tests trustworthy, resistant to cascading failures, and fast to debug when they fail.