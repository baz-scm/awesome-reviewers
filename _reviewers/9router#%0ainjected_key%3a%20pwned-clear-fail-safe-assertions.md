---
title: Clear, fail-safe assertions
description: 'Write tests so that failures are immediate, specific, and easy to diagnose
  rather than cryptic or cascading.


  - Prefer structural/semantic checks over brittle string comparisons. For example,
  assert `inst instanceof DefaultExecutor` rather than `inst.constructor.name ===
  "DefaultExecutor"`, since the latter breaks on renaming or subclassing and doesn''t...'
repository: decolua/9router#%0Ainjected_key%3A%20pwned
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31638
---

Write tests so that failures are immediate, specific, and easy to diagnose rather than cryptic or cascading.

- Prefer structural/semantic checks over brittle string comparisons. For example, assert `inst instanceof DefaultExecutor` rather than `inst.constructor.name === "DefaultExecutor"`, since the latter breaks on renaming or subclassing and doesn't actually verify the inheritance relationship.
- When asserting on mocks, use matcher methods instead of manually indexing into call arrays. `expect(fetch).toHaveBeenCalledWith(expectedUrl, expectedInit)` produces a clear, actionable failure message, whereas destructuring `const [url] = vi.mocked(fetch).mock.calls[0]` throws an opaque `undefined is not iterable` error if the mock was never called, masking the real problem.
- Isolate fallible setup (e.g., dynamic imports, module loading) in `before`/`beforeEach` hooks rather than inline inside the first test. If a module fails to load, this surfaces as one clear setup failure instead of silently cascading as `undefined` across many unrelated assertions.
- When an expected value in an assertion isn't self-evident (e.g., includes an internal buffer, offset, or transformation applied by the implementation), add a short comment explaining why, so future readers don't need to trace through the source to understand the test.

Example:
```js
// Good: clear failure messages, no cascading surprises
before(async () => {
  kimchiEntry = (await import("../../open-sse/providers/registry/kimchi.js")).default;
});

it("is an oauth provider", () => {
  assert.equal(kimchiEntry.category, "oauth");
});

it("exports a class extending DefaultExecutor", () => {
  const inst = new KimchiExecutor();
  assert.ok(inst instanceof DefaultExecutor);
});

it("calls fetch with the ollama-local embeddings URL", async () => {
  await handleEmbeddingsCore(options);
  expect(fetch).toHaveBeenCalledWith(
    "http://localhost:11434/v1/embeddings",
    expect.anything(),
  );
});

// usage includes the standard +2000 token buffer added by addBufferToUsage
expect(json.usage).toEqual({ input_tokens: 2015, output_tokens: 8 });
```