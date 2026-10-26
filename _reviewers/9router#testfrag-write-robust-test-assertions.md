---
title: Write robust test assertions
description: 'Prefer assertions that produce clear failure messages and verify real
  behavior over fragile or implementation-detail checks.


  - When asserting on mocks, use the dedicated matcher (e.g. `expect(fetch).toHaveBeenCalledWith(url,
  expect.objectContaining({...}))`) instead of manually destructuring `mock.calls[0]`.
  Destructuring an empty calls array throws an...'
repository: decolua/9router#testfrag
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31419
---

Prefer assertions that produce clear failure messages and verify real behavior over fragile or implementation-detail checks.

- When asserting on mocks, use the dedicated matcher (e.g. `expect(fetch).toHaveBeenCalledWith(url, expect.objectContaining({...}))`) instead of manually destructuring `mock.calls[0]`. Destructuring an empty calls array throws an opaque `TypeError: undefined is not iterable`, hiding the real reason the test failed, whereas `toHaveBeenCalledWith` reports exactly what was expected vs. received.
- Avoid exact-match assertions (`toBe`) on values assembled dynamically (e.g. built URLs) when a matcher can validate the call more completely and give a better diff on failure.
- Test behavior through stable, public contracts rather than brittle internals: check `instance instanceof BaseClass` rather than `instance.constructor.name === "ClassName"`, since the latter breaks under minification, subclassing, or renaming.
- When an expected value includes a non-obvious transformation (e.g., a token-count buffer added by the code under test), add a short comment at the assertion explaining why, so future readers don't mistake a correct value for a bug.

Example:
```js
// Bad: throws unhelpful error if fetch wasn't called, and brittle on exact string
const [url] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");

// Good: clear failure message, validates the full call
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) }),
);
```