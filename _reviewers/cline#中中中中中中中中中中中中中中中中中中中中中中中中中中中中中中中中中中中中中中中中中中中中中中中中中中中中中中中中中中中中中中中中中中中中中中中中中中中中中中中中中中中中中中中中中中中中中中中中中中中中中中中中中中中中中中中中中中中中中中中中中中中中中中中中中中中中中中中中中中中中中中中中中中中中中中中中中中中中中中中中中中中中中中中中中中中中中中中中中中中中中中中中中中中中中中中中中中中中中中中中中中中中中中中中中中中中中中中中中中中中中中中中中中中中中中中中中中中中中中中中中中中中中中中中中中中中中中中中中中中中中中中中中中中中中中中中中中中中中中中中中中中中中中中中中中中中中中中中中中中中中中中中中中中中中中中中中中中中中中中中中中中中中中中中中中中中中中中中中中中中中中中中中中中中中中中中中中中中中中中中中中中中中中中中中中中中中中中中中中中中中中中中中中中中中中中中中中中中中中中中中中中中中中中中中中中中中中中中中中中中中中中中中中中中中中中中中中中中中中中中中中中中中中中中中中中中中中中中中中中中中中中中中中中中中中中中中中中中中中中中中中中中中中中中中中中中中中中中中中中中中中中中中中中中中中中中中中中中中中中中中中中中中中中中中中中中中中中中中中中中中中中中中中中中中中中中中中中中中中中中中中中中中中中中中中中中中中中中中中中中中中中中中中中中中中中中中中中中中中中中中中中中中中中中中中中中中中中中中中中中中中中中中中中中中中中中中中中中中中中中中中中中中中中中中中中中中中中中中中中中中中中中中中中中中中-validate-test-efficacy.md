---
title: Validate test efficacy
description: 'A test that always passes, or that only coincidentally catches a bug,
  is worse than no test: it gives false confidence. Before relying on a new or changed
  test, confirm it actually fails against the broken behavior and passes once the
  fix lands (a quick mutation check: revert the fix, or reintroduce the bug, and watch
  the test turn red).'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Testing
language: TypeScript
comments_count: 13
repository_stars: 70986
---

A test that always passes, or that only coincidentally catches a bug, is worse than no test: it gives false confidence. Before relying on a new or changed test, confirm it actually fails against the broken behavior and passes once the fix lands (a quick mutation check: revert the fix, or reintroduce the bug, and watch the test turn red).

Concretely:
- Pick fixtures that isolate the thing under test. If every fixture shares an incidental signal (e.g. every "overloaded" test message also contains the word "overloaded"), the assertion may be passing for the wrong reason — add a neutral-message/isolated case that removes the confound.
- Avoid assertions that can silently no-op. `value?.should.deepEqual(...)` short-circuits to a pass on `undefined`; use `should(value).deepEqual(...)` or an equivalent that fails loudly on a missing value.
- Prefer exact/deterministic assertions over loose bounds when the underlying value is deterministic. `expect(perImageCost).toBe(FLAT_RATE)` catches a regression that `expect(cost).toBeLessThan(cost * 20)` would miss.
- When a fix removes a cap, limit, or special-case, write the test to prove the cap is gone (e.g. "keeps every failure, no cap" rather than merely "keeps at least N failures") so reintroducing the cap fails the test.
- For async/ordering bugs (races, rejections, disconnects), write the test to exercise the exact sequence that triggers the bug — e.g. start waiting before a tracked promise rejects, or unregister a client while a request is in flight — and assert on the specific failure mode (no unhandled rejection, a specific error message) rather than a generic "doesn't throw."
- When testing against a real dependency (an SDK, a CLI package version, a compiled entrypoint), assert against the actual source of truth (e.g. `package.json`, the real compiled bundle) instead of a hardcoded duplicate value that can drift out of sync.

Example, preferring an exact assertion over a loose bound:
```ts
it("charges a flat ESTIMATED_TOKENS_PER_IMAGE per image, independent of payload length", () => {
	const estimate = (data: string) =>
		estimateRequestInputTokens({
			messages: [{ role: "user", content: [{ type: "image", data, mediaType: "image/png" }] }],
		});
	expect(estimate("A".repeat(500_000))).toBe(estimate("A"));
});
```