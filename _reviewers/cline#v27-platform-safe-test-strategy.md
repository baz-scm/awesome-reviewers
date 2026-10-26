---
title: Platform-Safe Test Strategy
description: 'When adding or changing tests, prefer reliability over convenience:
  use platform-safe approaches, avoid brittle mocks that distort runtime behavior,
  and assert precise contracts.'
repository: cline/cline#v27
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70892
---

When adding or changing tests, prefer reliability over convenience: use platform-safe approaches, avoid brittle mocks that distort runtime behavior, and assert precise contracts.

Guidelines
- Avoid mocks that break semantics or require OS-specific plumbing. If mocking a process/exec/child behavior would change results or be flaky (e.g., Windows differences), use realistic integration fixtures/inputs instead.
- If stubbing async/process/stream behavior, stub the smallest unit that controls test termination. Don’t use never-ending streams that can leave listeners/process lifecycle running past the test.
- Assert exact call contracts for policy/opt-out paths (e.g., verify the helper is called exactly once with the expected payload, and verify forbidden helper calls never happen).
- Reuse shared exported constants/versions in tests instead of hardcoding strings, and verify exact version pinning to prevent drift across packages.
- Add targeted edge-case tests for command/file semantics and cross-platform path handling (literal pathspecs, POSIX vs OS separators, spaces/backslashes in filenames, etc.).

Example (contract + opt-out style)
```ts
// Pseudocode: ensure opt-out paths don’t call restricted behavior
expect(captureSpy).toHaveBeenCalledOnceWithExactly(
  CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
  { sessionId, count, reason },
);
expect(captureRequiredSpy).not.toHaveBeenCalled();
```

Rule of thumb: choose the testing level (unit vs integration) that preserves real runtime semantics, then make the assertions strict enough to prevent regressions.