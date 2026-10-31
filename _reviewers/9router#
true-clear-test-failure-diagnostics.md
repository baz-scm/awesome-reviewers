---
title: Clear test failure diagnostics
description: 'Write tests so that when they fail, the failure message points directly
  at the root cause rather than producing confusing, cascading, or generic errors.
  Concretely:'
repository: 'decolua/9router#

  true'
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 31736
---

Write tests so that when they fail, the failure message points directly at the root cause rather than producing confusing, cascading, or generic errors. Concretely:

- Load shared fixtures, modules, or dynamic imports in a `beforeEach`/`before` hook rather than inline inside the test body. If the load fails, it should surface as one isolated failure, not as `undefined` property errors scattered across unrelated assertions.
- Prefer high-level matchers over manual indexing/destructuring of mock results. For example, use `expect(fetch).toHaveBeenCalledWith(url, init)` instead of `const [url, init] = vi.mocked(fetch).mock.calls[0]`, since destructuring an empty call list throws an opaque "undefined is not iterable" error instead of a readable assertion failure.
- When an expected value is non-obvious (e.g., it includes a buffer, offset, or transformation applied by the code under test), add a short inline comment explaining why the value is what it is, so future readers don't have to re-derive the logic to trust the assertion.

Example:
```js
// Bad: throws a confusing TypeError if fetch was never called
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe(expectedUrl);

// Good: fails with a clear message naming the missing call
expect(fetch).toHaveBeenCalledWith(expectedUrl, expect.objectContaining({ body: expectedBody }));

// Good: explain non-obvious expected values
// input_tokens is 15 in the fixture, handler adds +2000 buffer via addBufferToUsage
expect(json.usage).toEqual({ input_tokens: 2015, output_tokens: 8 });
```