---
title: Test isolation and determinism
description: 'Tests should be deterministic, isolated, and assert the intended behavior
  (not just a coincidence or shared prior state). Concretely:


  - Reset external/shared state for every test (especially Redis, quotas, counters).
  Do not rely on the order tests run.'
repository: apache/apisix
label: Testing
language: Other
comments_count: 7
repository_stars: 16922
---

Tests should be deterministic, isolated, and assert the intended behavior (not just a coincidence or shared prior state). Concretely:

- Reset external/shared state for every test (especially Redis, quotas, counters). Do not rely on the order tests run.
- Avoid vacuous assertions and shared artifacts (e.g., “last line in a shared file”) that can match data from earlier blocks.
- When testing stateful backends, prefer multi-worker coverage so race/state behavior is exercised.
- Keep test scaffolding minimal—remove dead/irrelevant setup that doesn’t actually reach the code under test.
- Use fixed test inputs/identifiers where applicable to avoid flakiness.

Example (state reset + independent setup):
```perl
add_block_preprocessor(sub {
    my ($block) = @_;

    # Ensure Redis-backed tests start from a known state
    require("lib.test_redis").flush_all();

    # Optionally set a deterministic default request
    if (!$block->request) {
        $block->set_value("request", "GET /t");
    }
});
```

Example (avoid shared-state/vacuous “tail -n 1”):
- Don’t assert against a shared “last export” file unless you can correlate the export to the current request.
- If you must pattern-match, make the pattern reject the forbidden value (e.g., all-zero) instead of only matching a broad UUID/hex shape.

Apply this standard when adding or modifying tests in the Testing category to reduce CI flakiness and increase confidence in coverage.