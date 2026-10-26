---
title: Behavior-First Test Standards
description: 'When adding/updating tests, optimize for correctness signals that match
  real behavior and avoid brittle scaffolding.


  **Guidelines**

  1. **Test the real decision point, not helper internals**: If a UI outcome depends
  on combined state/conditions/timing, write a test that exercises the full pipeline
  (e.g., the hook as used) with realistic state and...'
repository: Cline/Cline
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70840
---

When adding/updating tests, optimize for correctness signals that match real behavior and avoid brittle scaffolding.

**Guidelines**
1. **Test the real decision point, not helper internals**: If a UI outcome depends on combined state/conditions/timing, write a test that exercises the full pipeline (e.g., the hook as used) with realistic state and transitions.
2. **Avoid brittle “incidental detail” assertions**: Don’t assert exact log payload field shapes or internal process counts unless behavior depends on those details. Prefer tests that validate observable outcomes.
3. **Don’t add test-only plumbing that harms portability**: Avoid mocks/wrappers that break cross-platform behavior (e.g., mocking `child_process` in ways that invalidate promises/Windows behavior). Prefer validating via stable, real execution paths where practical.
4. **Stub at stable boundaries to keep tests deterministic**: Replace long-running streams/process execution with bounded stubs so async listeners/cleanup don’t outlive the test.
5. **Tie expectations to shared sources of truth**: Use exported constants or derived package metadata so tests fail when the contract changes (not when version strings drift).
6. **Be strict about data shape/contract requirements**: Don’t use transformations that can hide missing required groups (e.g., plural categories). Assert that required schema/CLDR cardinal groups exist exactly as expected.

**Example (behavior-level hook test shape)**
```ts
// Pseudocode: test the hook’s output via realistic state/transition inputs
it("keeps loader hidden during provisioning handoff, then shows on successor", async () => {
  const result = renderHook(() => useDebouncedLoaderVisibility(computeInputsForProvisioning()));

  // provisioning tail + stale idle turnState + forceShow: should be hidden
  expect(result.current).toBe(false);

  // simulate successor that should re-enable loader
  act(() => pushNextEvent("api_req_started"));
  expect(result.current).toBe(true);
});
```

Apply these rules whenever you’re tempted to: (a) assert exact log field names, (b) count spawned processes, (c) test only helper predicates, or (d) “massage” data so missing required fields/groups can’t fail your tests.