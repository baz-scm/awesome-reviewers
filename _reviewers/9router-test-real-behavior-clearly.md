---
title: Test real behavior clearly
description: 'Tests should exercise the actual production code and fail with clear,
  actionable messages when something breaks.


  - Import and call the real implementation under test instead of re-declaring a copy
  of the logic inside the test file. A duplicated helper can silently drift from production
  code, giving false confidence that the feature is covered when it''s...'
repository: decolua/9router
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31412
---

Tests should exercise the actual production code and fail with clear, actionable messages when something breaks.

- Import and call the real implementation under test instead of re-declaring a copy of the logic inside the test file. A duplicated helper can silently drift from production code, giving false confidence that the feature is covered when it's actually just testing itself.
- Prefer structural/behavioral checks over brittle string checks: use `instanceof` to verify a class's prototype chain rather than comparing `constructor.name`, and isolate async setup (e.g., dynamic imports) in a `before()`/`beforeEach()` hook so a load failure surfaces as one clear failure instead of cascading as `undefined` across unrelated assertions later in the suite.
- When asserting on mocked calls, avoid destructuring `mock.calls[0]` directly—if the mock was never called, this throws an opaque `undefined is not iterable` error that obscures the real failure. Use `expect(fn).toHaveBeenCalledWith(...)` instead, which reports a precise, readable diff of expected vs. actual arguments.
- When an expected value isn't immediately obvious from the test data alone (e.g., a value transformed by a buffering/normalization step elsewhere in the code), add a short comment at the assertion explaining where the extra transformation comes from, so future readers don't have to re-derive it.

Example:
```js
// Bad: re-implemented logic + brittle destructure/equality
function stripReasoningContent(body) { /* copy of prod code */ }
const [url, init] = fetch.mock.calls[0]; // throws if fetch wasn't called
expect(url).toBe(expected);

// Good: real implementation + clear failure message
import { stripReasoningContent } from "../../open-sse/executors/kimchi.js";
expect(fetch).toHaveBeenCalledWith(expectedUrl, expect.objectContaining({ body: expectedBody }));
expect(instance instanceof DefaultExecutor).toBe(true);
```