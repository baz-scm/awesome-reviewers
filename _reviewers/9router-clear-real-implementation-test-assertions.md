---
title: Clear, real-implementation test assertions
description: 'Tests must exercise the actual production code and fail with clear,
  actionable diagnostics rather than cryptic errors.


  - Import and test the real implementation instead of duplicating logic inline. A
  test that reimplements the function under test (e.g., copy-pasting `stripReasoningContent`
  into the test file) can pass even when the real code is broken;...'
repository: Decolua/9Router
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 31414
---

Tests must exercise the actual production code and fail with clear, actionable diagnostics rather than cryptic errors.

- Import and test the real implementation instead of duplicating logic inline. A test that reimplements the function under test (e.g., copy-pasting `stripReasoningContent` into the test file) can pass even when the real code is broken; export the function from the module and import it directly.
- Prefer structural/behavioral checks over brittle ones — use `instanceof` to verify inheritance instead of `constructor.name`, which breaks under minification or subclassing changes.
- Isolate setup/loading steps (e.g., dynamic imports, registry lookups) in a `before`/`beforeAll` hook so a failure there surfaces as one clear error, not a cascade of confusing `undefined` assertion failures in unrelated tests.
- Use matcher-based assertions (`expect(fetch).toHaveBeenCalledWith(...)`) instead of destructuring mock call arguments (`const [url] = mock.calls[0]`). If the mock was never called, destructuring throws an opaque `TypeError: undefined is not iterable`, whereas the matcher reports exactly what was expected vs. what happened.
- When an expected value isn't immediately obvious from the fixture (e.g., a token count padded by an internal buffer), add a short comment at the assertion explaining the discrepancy so future readers don't have to trace the logic themselves.

Example — prefer this:
```js
expect(fetch).toHaveBeenCalledWith("http://localhost:11434/v1/embeddings", expect.anything());
```
over:
```js
const [url] = vi.mocked(fetch).mock.calls[0]; // throws if fetch was never called
expect(url).toBe("http://localhost:11434/v1/embeddings");
```