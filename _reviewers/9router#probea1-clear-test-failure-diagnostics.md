---
title: Clear test failure diagnostics
description: 'Write tests so that failures immediately point to the real problem instead
  of producing confusing, unrelated errors that require extra digging.


  - Prefer built-in matchers over manually extracting values from mocks. Destructuring
  from `mock.calls[0]` and comparing with `.toBe()` means that if the mock was never
  called, you get an opaque `undefined is not...'
repository: decolua/9router#probeA1
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31730
---

Write tests so that failures immediately point to the real problem instead of producing confusing, unrelated errors that require extra digging.

- Prefer built-in matchers over manually extracting values from mocks. Destructuring from `mock.calls[0]` and comparing with `.toBe()` means that if the mock was never called, you get an opaque `undefined is not iterable` TypeError instead of a meaningful assertion failure, and exact string comparisons give poor diffs on mismatch. Use `expect(fn).toHaveBeenCalledWith(...)` instead, which fails cleanly and shows exactly what was expected vs. received:

```js
// Avoid
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");

// Prefer
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) })
);
```

- Isolate fallible setup (e.g., dynamic imports, module loading) in a `before`/`beforeEach` hook rather than at module scope or inline in the first test. This way a setup failure surfaces as a single, clearly-attributed failure instead of cascading as `undefined` across every subsequent assertion that depends on it.

- When an expected value isn't self-evident (e.g., includes an internal buffer/offset applied by the code under test), add a short comment explaining the computation so future readers don't have to reverse-engineer it.

Applying these practices keeps test failures actionable and prevents time wasted chasing misleading error messages.