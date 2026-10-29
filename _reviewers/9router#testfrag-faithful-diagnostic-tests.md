---
title: Faithful, diagnostic tests
description: 'Tests should exercise the real implementation and fail with a clear,
  immediately useful message when something is wrong.


  - Import and call the actual production function/class rather than re-implementing
  or copy-pasting its logic into the test file. A duplicated helper can silently drift
  from the real code and give false confidence (e.g. a test that...'
repository: decolua/9router#testfrag
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31643
---

Tests should exercise the real implementation and fail with a clear, immediately useful message when something is wrong.

- Import and call the actual production function/class rather than re-implementing or copy-pasting its logic into the test file. A duplicated helper can silently drift from the real code and give false confidence (e.g. a test that redefines `stripReasoningContent` locally instead of importing it from the executor module).
- Prefer structural/behavioral checks over brittle ones: use `instanceof` to verify inheritance instead of comparing `constructor.name` strings.
- When asserting on mocks, use the dedicated matcher (`expect(fetch).toHaveBeenCalledWith(...)`) instead of manually destructuring `mock.calls[0]` and comparing fields with `.toBe()`. Destructuring an empty/undefined call array throws an opaque "undefined is not iterable" error that hides the real failure, and `.toBe()` on strings gives you no diff context when the match fails.
- Load shared fixtures/dependencies (e.g. dynamic imports of registry entries) in a `before`/`beforeAll` hook rather than inline in the first test, so a loading failure surfaces as one clear, isolated failure instead of cascading into confusing `undefined` errors in unrelated assertions later in the suite.
- When an expected value depends on non-obvious logic elsewhere in the codebase (e.g. a hidden token buffer added by `addBufferToUsage`), add a short comment at the assertion explaining where the number comes from, so future readers don't have to trace it themselves.

Example of preferred mock assertion:
```js
// Avoid:
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe(expectedUrl);

// Prefer:
expect(fetch).toHaveBeenCalledWith(expectedUrl, expect.objectContaining({ body: expect.any(String) }));
```