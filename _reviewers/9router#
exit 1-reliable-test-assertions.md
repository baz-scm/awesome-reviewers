---
title: Reliable test assertions
description: 'Write tests that exercise real production code and fail with clear,
  actionable messages. Specifically:


  1. **Test the real implementation, not a copy.** If a helper exists in production
  code (e.g., `stripReasoningContent`), import and export it for testing rather than
  duplicating its logic inline in the test file. Duplicated helpers drift from the
  real...'
repository: 'decolua/9router#

  exit 1'
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 31737
---

Write tests that exercise real production code and fail with clear, actionable messages. Specifically:

1. **Test the real implementation, not a copy.** If a helper exists in production code (e.g., `stripReasoningContent`), import and export it for testing rather than duplicating its logic inline in the test file. Duplicated helpers drift from the real implementation and give false confidence.

2. **Prefer robust, specific matchers over brittle checks.** Use `instanceof` instead of `constructor.name` to verify class hierarchies, and use `expect(fn).toHaveBeenCalledWith(...)` instead of manually destructuring `mock.calls[0]`. Destructuring an empty/undefined call array throws an opaque `undefined is not iterable` error that hides the real failure reason, whereas built-in matchers report exactly what was expected vs. what happened:
```js
// Avoid: throws a confusing TypeError if fetch was never called
const [url, init] = vi.mocked(fetch).mock.calls[0];

// Prefer: clear, descriptive failure message
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```

3. **Isolate setup/import failures.** Load modules or fixtures needed by a suite in a `before`/`beforeEach` hook rather than inline in each test body. This way a load failure surfaces as a single, clearly-attributed failure instead of cascading as confusing `undefined` errors across unrelated assertions.

4. **Document non-obvious expected values.** When an assertion depends on implementation details that aren't apparent from the test alone (e.g., a hidden token buffer added by the handler), add a short comment explaining the expected value's origin so future readers don't have to re-derive it.

Applying these practices keeps test failures fast to diagnose and ensures tests actually validate the behavior of shipped code.