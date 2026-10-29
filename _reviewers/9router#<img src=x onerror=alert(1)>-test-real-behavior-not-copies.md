---
title: Test real behavior, not copies
description: Unit tests must exercise the actual production code path, not a reimplementation
  of it. If a test needs to call a helper (e.g. `stripReasoningContent`), import and
  test the exported function from the module itself rather than pasting a "mirror"
  copy into the test file — a duplicated helper can silently diverge from the real
  implementation and give false...
repository: decolua/9router#<img src=x onerror=alert(1)>
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 31644
---

Unit tests must exercise the actual production code path, not a reimplementation of it. If a test needs to call a helper (e.g. `stripReasoningContent`), import and test the exported function from the module itself rather than pasting a "mirror" copy into the test file — a duplicated helper can silently diverge from the real implementation and give false confidence, and a test labeled "integration" that only calls the local copy is misleading and should either call the real code path or be renamed/removed.

Pair this with assertions that are both robust and meaningful:
- Prefer behavior-based checks over brittle ones, e.g. `inst instanceof DefaultExecutor` instead of `inst.constructor.name === "..."`, and `expect(fetch).toHaveBeenCalledWith(url, init)` instead of manually destructuring mock calls and asserting with `toBe` on a hardcoded value that can silently diverge from what's actually sent.
- When an expected value isn't self-evident (e.g. `input_tokens: 2015` when the fixture sets `15`), add a short comment explaining the transformation (here, a documented +2000 buffer) so the next reader doesn't have to trace through the source to confirm it's correct.
- Cover realistic edge cases uncovered by review, such as alternate ordering of interleaved blocks/tool calls, with a dedicated test case rather than relying on a single happy-path fixture.

Example of what to avoid vs. prefer:
```js
// Avoid: duplicated logic + weak assertion
function stripReasoningContent(body) { /* copy of real implementation */ }
assert.equal(inst.constructor.name, "KimchiExecutor");

// Prefer: real implementation + robust assertion
import { stripReasoningContent } from "../../open-sse/executors/kimchi.js";
assert.ok(inst instanceof DefaultExecutor);
expect(fetch).toHaveBeenCalledWith("http://192.168.1.100:11434/v1/embeddings", expect.anything());
```