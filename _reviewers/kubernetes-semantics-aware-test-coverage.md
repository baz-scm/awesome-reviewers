---
title: Semantics-Aware Test Coverage
description: When adding or modifying tests, ensure they (1) cover the minimal correctness
  set (including edge/error paths), (2) validate key invariants so the test itself
  can’t silently be wrong, and (3) in E2E, assert the real semantics—not just the
  final API phase—while keeping timing bounded to avoid flakiness.
repository: kUbernetes/kUbernetes
label: Testing
language: Go
comments_count: 11
repository_stars: 128688
---

When adding or modifying tests, ensure they (1) cover the minimal correctness set (including edge/error paths), (2) validate key invariants so the test itself can’t silently be wrong, and (3) in E2E, assert the real semantics—not just the final API phase—while keeping timing bounded to avoid flakiness.

**Practical rules**
1) **Include minimal error + edge cases for correctness**
   - Add downsizing/resize-down cases and explicit error-path scenarios (insufficient resources, invalid inputs) as part of the “required” test set.
   - If a code path is plausibly unreachable due to ordering, add unit tests that would have failed without the ordering fix.

2) **Assert invariants in the tests, not assumptions**
   - Don’t rely on “the caller guarantees X” unless you still test the invariant at some layer (at least once) to catch accidental future regressions or test wiring mistakes.

3) **In E2E, verify semantic behavior (signals/events/logs/watch), not just termination/scheduling**
   - For behavior involving signals/hooks/timeouts, validate the exact sequence using pod logs, watch event streams, or explicit runtime artifacts.
   - Add post-window checks so “never probed / never started / already terminated” doesn’t pass silently.

4) **Use structured tests for completeness and maintainability**
   - Prefer table-driven unit tests for coverage breadth.
   - Factor shared helpers and use `t.Helper()` in custom `must*` helpers so failures point to the right call site.

**Example (Go unit test invariant helper)**
```go
func mustParseCPUSet(t *testing.T, s string) cpuset.CPUSet {
	t.Helper()
	set, err := cpuset.Parse(s)
	if err != nil { t.Fatalf("parse %q: %v", s, err) }
	return set
}

func requireDisjoint(t *testing.T, a, b cpuset.CPUSet) {
	t.Helper()
	if a.Intersection(b).Len() != 0 {
		t.Fatalf("expected disjoint sets, overlap=%s", a.Intersection(b))
	}
}
```

**Example (E2E semantics verification idea)**
- After triggering the behavior, stream logs or watch container termination to assert *exactly* the expected signal/event sequence and add a bounded timeout so failures don’t run for hours.

Applying these standards will prevent both (a) correctness gaps where only the happy path is tested and (b) E2E regressions that “look fine” because the test checked a superficial outcome rather than the true semantics.