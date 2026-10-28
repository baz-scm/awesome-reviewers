---
title: Tests must catch real failures
description: A test is only useful if it actually fails when the bug it targets is
  present. Before merging a test, mutate the code under test (or imagine removing
  the fix) and confirm the assertion fails — not just that it "runs."
repository: cline/cline#;sleep 4;
label: Testing
language: TypeScript
comments_count: 14
repository_stars: 70976
---

A test is only useful if it actually fails when the bug it targets is present. Before merging a test, mutate the code under test (or imagine removing the fix) and confirm the assertion fails — not just that it "runs."

Concretely:
- Avoid assertions that can short-circuit past a missing value, e.g. `value?.should.deepEqual(...)` passes silently when `value` is `undefined`; use `should(value).deepEqual(...)` so absence itself fails the test.
- Isolate the variable you claim to test. If every fixture for "retry on overloaded-capacity code" also has the word "overloaded" in the message, the code-based branch is never actually exercised on its own — add a case with a neutral message so the code path alone is pinned. Same for "cost must not scale with payload size": assert the exact per-unit cost (`estimate("A") === estimate("A".repeat(500_000))`), not a loose `toBeLessThan(x / 10)` that could pass for the wrong reason.
- Prefer exercising the real decision point over a shallow or over-mocked substitute. A round-trip conversion test should run through the actual converter/loader (e.g. load installed skill config and assert it registers under the right name/description), not just check a byproduct like a directory name. Where mocking at module boundaries hides real integration bugs (e.g., mocking `@ai-sdk/openai` means the real request/response shape never runs), add a wire-level test against the real adapter with a stubbed transport.
- When faking a dependency (fs, child_process, a server script) would force fragile test-only plumbing or diverge from real behavior (mocking `node:child_process` breaks promisified `execFile`; a shell wrapper won't run on Windows), prefer driving the real mechanism in-process (a temp directory, a real small server script) over a mock that can't represent the actual failure mode.
- Keep claims in test/PR comments precise and limited to what the test actually proves; don't say "no assertion depends on the catalog" if a downstream resolver still consults it.
- Delete tests that duplicate another layer's responsibility (e.g., pinning a third-party adapter's own translation logic) or that only add volume without protecting a distinct, important behavior.