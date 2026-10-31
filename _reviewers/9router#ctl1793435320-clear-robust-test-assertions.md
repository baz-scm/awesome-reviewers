---
title: Clear, robust test assertions
description: 'Write tests so that failures are immediately diagnosable and assertions
  don''t produce misleading or opaque errors. Specifically:


  1. Prefer semantic assertion APIs over manual extraction/matching. When checking
  mock calls, use `expect(fn).toHaveBeenCalledWith(...)` instead of destructuring
  `mock.calls[0]` and comparing fields manually — if the mock was...'
repository: decolua/9router#ctl1793435320
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 31733
---

Write tests so that failures are immediately diagnosable and assertions don't produce misleading or opaque errors. Specifically:

1. Prefer semantic assertion APIs over manual extraction/matching. When checking mock calls, use `expect(fn).toHaveBeenCalledWith(...)` instead of destructuring `mock.calls[0]` and comparing fields manually — if the mock was never called, manual destructuring throws a confusing "undefined is not iterable" error instead of a clear assertion failure.

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

2. Avoid brittle structural checks like `instance.constructor.name === "Foo"`; use `instanceof` or other prototype-aware checks that survive subclassing/minification and actually assert the intended contract.

3. Isolate fallible setup (dynamic imports, module loading, fixture construction) in `before`/`beforeEach` hooks rather than inline in the describe body, so a setup failure surfaces as one clear failing test rather than cascading into unrelated `undefined` errors in later assertions.

4. When an expected value isn't self-evident from the test alone (e.g., includes a buffer/offset applied by the implementation), add a short comment at the assertion explaining why that value is correct, so future readers don't have to re-derive it from the source.

Applying these practices ensures test failures point directly at the real problem, reducing debugging time and preventing misleading test reports.</description>
</invoke>
