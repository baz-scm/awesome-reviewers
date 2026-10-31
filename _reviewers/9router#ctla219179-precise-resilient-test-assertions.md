---
title: Precise, resilient test assertions
description: Tests must validate the actual production code path and fail with clear,
  actionable diagnostics rather than masking problems or crashing with confusing errors.
repository: decolua/9router#ctlA219179
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 31730
---

Tests must validate the actual production code path and fail with clear, actionable diagnostics rather than masking problems or crashing with confusing errors.

Apply the following when writing unit/integration tests:

1. **Exercise the real implementation, not a copy.** Never re-implement production logic inline in a test file "for isolation" — export the function/class from the source module and import it. A duplicated helper can silently drift from the real code and give false confidence (e.g. a test that pins `stripReasoningContent` behavior should import it from `open-sse/executors/kimchi.js`, not redefine it in the test file).

2. **Prefer structural/semantic checks over brittle string checks.** Use `instanceof` to verify class inheritance instead of `constructor.name`; use `expect(fn).toHaveBeenCalledWith(...)` instead of manually destructuring `mock.calls[0]` and comparing fields with `.toBe()`. Manual destructuring throws an unreadable "undefined is not iterable" error when the mock was never invoked, and exact-match assertions don't clearly report what was actually received — built-in matchers surface the real cause immediately:
```js
// Avoid
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://localhost:11434/v1/embeddings");

// Prefer
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```

3. **Isolate setup/import failures.** Load shared fixtures, dynamic imports, or registry entries in a `before`/`beforeEach` hook rather than inline at the top of a test body, so a single setup failure produces one clear failing test instead of cascading `undefined` errors across unrelated assertions.

4. **Document non-obvious expected values.** When an assertion encodes a transformation (buffers, offsets, padding, etc.) that isn't obvious from the fixture alone, add a short comment explaining where the value comes from, so future readers don't mistake it for a bug.

5. **Cover realistic edge cases for pattern-matching logic.** When testing string/regex-based detection (e.g. user-agent sniffing), include cases designed to catch false positives from naive substring matching (e.g. `avoid/1.0`, `thunderbolt/2.0`) to ensure token/word-boundary matching is actually enforced.