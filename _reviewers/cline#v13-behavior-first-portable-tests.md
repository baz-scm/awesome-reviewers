---
title: Behavior-first, portable tests
description: 'When adding/adjusting tests, prefer behavior- and contract-focused assertions
  that don’t require brittle logging checks or OS-specific scaffolding.


  Apply this standard:'
repository: cline/cline#v13
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70874
---

When adding/adjusting tests, prefer behavior- and contract-focused assertions that don’t require brittle logging checks or OS-specific scaffolding.

Apply this standard:
- Assert the externally meaningful contract: payload shape for telemetry helpers, correct request routing for adapter boundaries, and correctness for tricky user inputs (e.g., filenames/pathspecs).
- Use “real adapter + stubbed I/O” tests at integration boundaries: exercise the actual adapter path, but stub network/filesystem so the test stays fast and deterministic.
- Keep tests portable and low-plumbing: if a unit test would require heavy child_process mocking or platform-dependent PATH tricks, either rely on existing correctness coverage or use a higher-level test that reflects real behavior.
- Avoid brittle harness that doesn’t add value: don’t lock down log field names/format via console spying when existing server behavior/regression tests already cover the code path.
- Don’t duplicate source-of-truth constants across packages: reuse exported constants and assert exact version coupling when that’s the contract.

Example pattern (wire test with stubbed fetch):
```ts
// Pseudocode: exercise real adapter wiring, but stub fetch.
const fetch = vi.fn(async () => ({
  ok: true,
  json: async () => ({ data: [{ text: 'hello' }] }),
}));
vi.stubGlobal('fetch', fetch);

await transcribeAudio({
  config: { type: 'openai-native', /* ... */ },
  audio: /* ... */,
});

expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/v1/audio/transcriptions'), expect.anything());
```

Result: tests stay maintainable, deterministic, and aligned with real behavior rather than internal implementation details.