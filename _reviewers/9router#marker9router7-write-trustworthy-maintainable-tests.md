---
title: Write trustworthy, maintainable tests
description: 'Tests should exercise real production code and fail with clear, actionable
  diagnostics.


  1. Import and test the actual implementation — never paste a "mirror" copy of production
  logic into the test file. A duplicated helper can drift from the real code and still
  pass, giving false confidence (e.g. a test that redefines `stripReasoningContent`
  locally...'
repository: decolua/9router#MARKER9ROUTER7
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31644
---

Tests should exercise real production code and fail with clear, actionable diagnostics.

1. Import and test the actual implementation — never paste a "mirror" copy of production logic into the test file. A duplicated helper can drift from the real code and still pass, giving false confidence (e.g. a test that redefines `stripReasoningContent` locally instead of importing/exporting it from the executor). If a function isn't exported yet, export it so the test calls the real thing.

2. Assert on behavior, not implementation details. Prefer `instanceof` over `constructor.name` when checking class relationships, and avoid "integration" tests that silently fall back to calling an internal helper directly instead of actually invoking the code path they claim to cover.

3. When asserting on mocks, use the matcher's built-in call-matching instead of manually destructuring `mock.calls[0]` and comparing with `.toBe()`. If the mock was never called, destructuring throws a cryptic "undefined is not iterable" error that hides the real failure, and manual field-by-field comparisons produce noisy diffs. Prefer:

```js
// Avoid:
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://localhost:11434/v1/embeddings");

// Prefer:
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```

4. Cover edge cases explicitly rather than assuming one ordering/shape is representative — e.g., add a dedicated test for reversed block order when fixing an ordering bug, so regressions are caught for every input arrangement, not just the one that happened to trigger the original report.

5. When an assertion's expected value isn't self-evident (e.g., it includes a hidden buffer or transformation applied by the code under test), add a short comment next to the assertion explaining where the number comes from, so future readers don't have to re-derive it.