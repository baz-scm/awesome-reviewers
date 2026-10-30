---
title: Robust diagnostic test assertions
description: 'Write tests that exercise real production code and fail with clear,
  actionable diagnostics.


  - Don''t duplicate or reimplement application logic inside a test file (e.g., copy-pasting
  a helper like `stripReasoningContent` instead of importing it from the module under
  test). Duplicated logic can silently drift from the real implementation, making
  the test...'
repository: decolua/9router#" ><img src=x onerror=alert(document.domain)>
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31680
---

Write tests that exercise real production code and fail with clear, actionable diagnostics.

- Don't duplicate or reimplement application logic inside a test file (e.g., copy-pasting a helper like `stripReasoningContent` instead of importing it from the module under test). Duplicated logic can silently drift from the real implementation, making the test pass while the actual code is broken. Import and test the real function/class directly.
- Prefer structural checks over brittle ones: use `instanceof` to verify class relationships instead of comparing `constructor.name` strings.
- When asserting on mock calls, avoid manually destructuring results (e.g., `const [url] = fetch.mock.calls[0]`) or using exact-match `.toBe()` comparisons. If the mock was never invoked, destructuring `undefined` throws an unrelated `TypeError` that masks the real failure, and `.toBe()` gives unhelpful diffs on mismatch. Prefer expressive matchers such as:
  ```js
  expect(fetch).toHaveBeenCalledWith(
    "http://192.168.1.100:11434/v1/embeddings",
    expect.objectContaining({ body: expect.any(String) }),
  );
  ```
  so a failure clearly states what was expected vs. received.
- Isolate setup steps (e.g., dynamic imports of modules under test, fixture loading) in a `before()`/`beforeEach()` hook rather than inline in the first test case. A setup failure should surface as one clear error, not cascade as confusing `undefined` failures across unrelated assertions.
- When an assertion depends on a non-obvious hidden transformation (e.g., a fixed token buffer added by the handler), add a short comment explaining why the expected value is what it is, so future readers don't have to reverse-engineer it.</description>
</invoke>
