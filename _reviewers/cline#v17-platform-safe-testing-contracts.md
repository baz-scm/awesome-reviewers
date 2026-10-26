---
title: Platform-Safe Testing Contracts
description: Write tests to validate externally observable behavior and contractual
  outcomes, using minimal harness that preserves real runtime semantics across platforms.
repository: cline/cline#v17
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70883
---

Write tests to validate externally observable behavior and contractual outcomes, using minimal harness that preserves real runtime semantics across platforms.

Apply these rules:
- Prefer wire/adapter-level (“real adapter, stub fetch”) tests over mocking constructors when the integration path matters.
- Don’t add test-only plumbing that changes OS/runtime behavior (e.g., mocking `child_process`/spawning behavior or PATH-dependent wrappers) unless the test purpose truly requires it.
- Assert outputs and request/parse contracts; avoid brittle assertions on internal log payload shapes or other implementation details—use existing server/path tests to catch regressions.
- Cover meaningful edge cases and invariants explicitly (literal pathspec handling, filenames with spaces/asterisks, strict version equality, plural-category completeness).
- Keep test and PR comments precise about what is and isn’t exercised (e.g., catalog-dependent model ID rewrites).

Example (contract-style wire test):
```ts
// Real adapter, stubbed network; assert the request contract.
const result = await transcribeAudio({
  config: { provider: "openai-native" },
  audio: /* ... */,
});
expect(stubFetch.calls[0].url).toBe("/v1/audio/transcriptions");
expect(result.text).toContain("...");
```

If the behavior depends on OS-sensitive details (spawning, git pathspec parsing), either rely on existing correctness tests or cover the edge case directly (e.g., test literal pathspec behavior with filenames like `draft*.txt`) rather than introducing harness that would require platform-specific mocking.