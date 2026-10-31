---
title: Test real behavior clearly
description: 'Tests must exercise the actual production code and fail with clear,
  actionable messages when something breaks.


  - Never re-implement or copy-paste the logic under test into the test file. Import
  and call the real exported function/class so the test actually catches regressions
  in production code.'
repository: decolua/9router#y
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31751
---

Tests must exercise the actual production code and fail with clear, actionable messages when something breaks.

- Never re-implement or copy-paste the logic under test into the test file. Import and call the real exported function/class so the test actually catches regressions in production code.
  ```js
  // Bad: duplicated helper drifts from the real implementation
  function stripReasoningContent(body) { /* copy of prod logic */ }

  // Good: import and test the real thing
  import { stripReasoningContent } from "../../open-sse/executors/kimchi.js";
  ```
- Avoid fragile structural checks like `instance.constructor.name === "ClassName"`; use `instanceof ParentClass` to correctly verify the prototype chain, including inheritance.
- Perform module loading or other setup that can fail (e.g., dynamic imports) inside `before`/`beforeAll` hooks rather than inline inside an `it()` body. This way a load failure surfaces as one clear, isolated failure instead of cascading into confusing `undefined` errors in unrelated assertions.
- Prefer expressive matchers over manual extraction of mock data. For example, use `expect(fetch).toHaveBeenCalledWith(url, init)` instead of destructuring `const [url, init] = fetch.mock.calls[0]`, which throws an opaque `undefined is not iterable` error if the mock was never called, masking the real failure reason.

Following these practices ensures test failures point directly at the real cause, and that passing tests genuinely validate the behavior of the shipped code.