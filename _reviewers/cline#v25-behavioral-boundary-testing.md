---
title: Behavioral boundary testing
description: When adding/adjusting tests, choose assertions and harnessing that preserve
  real runtime semantics and protect meaningful behavior—not incidental implementation
  details.
repository: cline/cline#v25
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 70891
---

When adding/adjusting tests, choose assertions and harnessing that preserve real runtime semantics and protect meaningful behavior—not incidental implementation details.

**Guidelines**
- **Test at the right boundary:** If adapter/CLI/runtime wiring matters and mocks would break semantics (or are OS-fragile), prefer **wire/integration** tests with the real adapter and stub only external IO (e.g., fetch).
- **Keep tests resilient:** Import shared constants/versions in tests instead of hardcoding to prevent drift across packages.
- **Avoid brittle internals:** Don’t assert log payload shape, or other incidental formatting, unless it’s a contractual surface; rely on existing behavior/flow tests.
- **Prevent test leakage:** Stub the specific prototype/entrypoints that start async work so tests don’t leave never-ending streams/listeners behind.
- **Use invariants for complex control flow:** For state machines or paged/skip/retry behavior, add a pinned sequence test and (when feasible) fuzz/randomized verb sequences to validate invariants.
- **Trim redundant coverage:** Keep tests focused on the feature’s contract (success/failure, retry limits, surfaced errors). Avoid expanding suites just to lock down telemetry implementation details.

**Illustrative pattern (invariant + sequence test)**
```ts
// Pinned sequence + fuzz-like invariant checks for state transitions.
// “skip hides only its row”, “undo skip restores row”, etc.
const invariantsHold = (state) => {
  // assert visible items follow invariants
  return true;
};

it("skip/undo maintains invariants", async () => {
  const seq = ["new", "new", "skip(verify)", "undo(skip)"];
  const states = await runComposerScenario(seq);
  expect(states.every(invariantsHold)).toBe(true);
});
```

Apply this by asking: *What observable behavior must remain true?* Then decide whether you need a unit test, a wire test with real adapters, or an invariant-based scenario test—without overfitting to implementation details like log formatting or internal event ordering.