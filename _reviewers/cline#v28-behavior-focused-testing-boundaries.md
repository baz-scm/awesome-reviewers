---
title: Behavior-Focused Testing Boundaries
description: 'When writing/adjusting tests, assert observable behavior while keeping
  the test harness portable and deterministic.


  Apply these rules:

  - Don’t assert incidental internals (process counts, exact log payload shapes) if
  they add brittle harnessing without improving behavioral regression detection; rely
  on existing coverage for correctness paths.'
repository: cline/cline#v28
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 70892
---

When writing/adjusting tests, assert observable behavior while keeping the test harness portable and deterministic.

Apply these rules:
- Don’t assert incidental internals (process counts, exact log payload shapes) if they add brittle harnessing without improving behavioral regression detection; rely on existing coverage for correctness paths.
- Avoid mocking that changes execution semantics across platforms (e.g., mocking `child_process` or introducing PATH/script wrappers that break Windows behavior). If the behavior depends on real tooling, validate via higher-level correctness tests.
- Use the right boundary for stubbing:
  - For adapter/plumbing correctness, prefer “wire” tests that exercise the real runtime adapter while stubbing the external boundary (e.g., HTTP `fetch`).
  - For pure logic (parsers, formatting, business rules), keep unit tests tightly focused.
- Make tests deterministic:
  - Use shared exported constants rather than hardcoded strings/versions.
  - Isolate environment variables using test utilities that correctly handle “unset before” cases.
  - Ensure async resources/listeners are not left running; stub the correct execution points so nothing outlives the test.
- Add targeted edge-case assertions (e.g., literal pathspec handling, complete plural category groups) that would fail on real regressions, without relying on implementation details.

Example pattern (wire integration with a stubbed external boundary):
```ts
// Exercise the real adapter wiring, but stub the network boundary.
const response = await transcribeAudio({
  config: { provider: "openai-native", /* ... */ },
  audio: /* ... */,
});
expect(response.text).toContain("...");
expect(fetch).toHaveBeenCalledWith(expect.stringContaining("/v1/audio/transcriptions"), expect.anything());
```

This approach keeps tests meaningful (behavioral), robust (cross-platform), and maintainable (minimal brittle harness).