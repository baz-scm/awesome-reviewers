---
title: Test real implementation clearly
description: 'Tests must exercise the actual production code path and fail with unambiguous
  diagnostics, not pass or fail for the wrong reason.


  1. Never re-implement the logic under test inside the test file. Import and call
  the real exported function/class so the test actually pins production behavior;
  a copy-pasted helper (e.g. a local `stripReasoningContent`) can...'
repository: decolua/9router#`id -u`
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 31732
---

Tests must exercise the actual production code path and fail with unambiguous diagnostics, not pass or fail for the wrong reason.

1. Never re-implement the logic under test inside the test file. Import and call the real exported function/class so the test actually pins production behavior; a copy-pasted helper (e.g. a local `stripReasoningContent`) can silently drift from the real implementation and give false confidence.

2. Prefer structural/type checks over brittle string checks. Use `instanceof` to verify inheritance (`expect(inst instanceof BaseClass).toBe(true)`) instead of comparing `constructor.name`, which breaks under minification/subclassing and doesn't prove the prototype chain is correct.

3. Use purpose-built matchers instead of manually destructuring mock results. For example, prefer:
```js
expect(fetch).toHaveBeenCalledWith(expectedUrl, expectedInit);
```
instead of:
```js
const [url, init] = vi.mocked(fetch).mock.calls[0]; // throws "undefined is not iterable" if fetch was never called
```
The matcher reports exactly what was expected vs. received when the call didn't happen, rather than an unrelated TypeError.

4. Isolate fixture/module loading that can fail (dynamic imports, registry lookups) in a `before`/`beforeAll` hook rather than inline in the first test case, so a load failure is reported once with a clear cause instead of cascading as `undefined` failures through every subsequent assertion.

5. When an expected value is derived from non-obvious transformation logic (buffers, offsets, caching adjustments), add a short comment at the assertion explaining where the number comes from, so future readers don't mistake correct-but-surprising output for a bug.

Applying these practices keeps tests trustworthy, makes failures self-explanatory, and prevents maintenance drift between test doubles and real implementations.