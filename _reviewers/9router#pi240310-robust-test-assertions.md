---
title: Robust test assertions
description: 'Write tests that exercise the real production code and fail with clear,
  actionable messages. Two concrete rules:


  1. Never re-implement or duplicate the logic under test inside the test file. Import
  and call the actual exported function/module, so the test verifies real behavior
  and stays correct if the implementation changes. If a helper isn''t exported...'
repository: decolua/9router#pi240310
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 31756
---

Write tests that exercise the real production code and fail with clear, actionable messages. Two concrete rules:

1. Never re-implement or duplicate the logic under test inside the test file. Import and call the actual exported function/module, so the test verifies real behavior and stays correct if the implementation changes. If a helper isn't exported yet, export it rather than copy-pasting it into the spec.

2. When asserting on mocked calls (e.g. `fetch`), avoid manually destructuring `mock.calls[0]` and comparing fields with `toBe()`. If the mock was never invoked, `mock.calls[0]` is `undefined` and destructuring throws a confusing "undefined is not iterable" error instead of a useful test failure. Prefer matcher-based assertions like `expect(fetch).toHaveBeenCalledWith(...)`, which both confirm the call happened and produce a readable diff when expectations don't match.

Example:

```js
// Avoid
const [url, init] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://localhost:11434/v1/embeddings");

// Prefer
expect(fetch).toHaveBeenCalledWith(
  "http://localhost:11434/v1/embeddings",
  expect.objectContaining({ body: expect.stringContaining('"model":"nomic-embed-text"') })
);
```

Applying both rules keeps tests honest (testing real code paths) and diagnostic (clear failures), reducing time spent debugging misleading test errors.