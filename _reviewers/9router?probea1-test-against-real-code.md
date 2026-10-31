---
title: Test against real code
description: 'Unit tests must exercise the actual production implementation rather
  than a re-implemented copy of the logic under test. Duplicating a helper function
  inside a test file (e.g., copy-pasting `stripReasoningContent` instead of importing
  it from the executor) creates a false sense of safety: the test can keep passing
  even after the real implementation changes...'
repository: decolua/9router?probeA1
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 31730
---

Unit tests must exercise the actual production implementation rather than a re-implemented copy of the logic under test. Duplicating a helper function inside a test file (e.g., copy-pasting `stripReasoningContent` instead of importing it from the executor) creates a false sense of safety: the test can keep passing even after the real implementation changes or breaks. Always import and call the exported function/module directly, and delete any "integration-style" tests that don't actually exercise the real code path or that carry misleading comments about what they verify (e.g., claiming a network call is made when it isn't).

When asserting on mocked calls (e.g., `fetch`, other injected dependencies), prefer the testing library's built-in matchers such as `expect(fetch).toHaveBeenCalledWith(url, expectedInit)` over manually extracting `mock.calls[0]` and comparing pieces with `.toBe()`. This avoids subtle mismatches between what you intended to assert and what you actually asserted, and produces clearer failure diffs.

When an expected value depends on non-obvious business logic (e.g., a token count that includes a hidden +2000 buffer), add a short comment at the assertion explaining why the value is what it is, so future readers aren't confused by numbers that don't match the fixture at a glance.

Example:
```js
// Bad: duplicated logic, drifts from real implementation
function stripReasoningContent(body) { /* copy of executor logic */ }

// Good: import and test the real function
import { stripReasoningContent } from "../../open-sse/executors/kimchi.js";

// Bad: manual extraction + exact match
const [url] = vi.mocked(fetch).mock.calls[0];
expect(url).toBe("http://192.168.1.100:11434/v1/embeddings");

// Good: idiomatic mock assertion
expect(fetch).toHaveBeenCalledWith(
  "http://192.168.1.100:11434/v1/embeddings",
  expect.objectContaining({ body: expect.any(String) })
);

// Good: comment clarifies a non-obvious expected value
// +2000 buffer applied by addBufferToUsage (see usageTracking.js)
expect(json.usage).toEqual({ input_tokens: 2015, output_tokens: 8 });
```