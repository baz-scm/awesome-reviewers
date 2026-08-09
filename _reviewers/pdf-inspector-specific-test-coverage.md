---
title: Specific Test Coverage
description: When tests target a particular guard, ordering, or threshold, ensure
  the test inputs actually exercise that exact logic (and not an earlier rejection/acceptance).
  Also pin threshold behavior with both sides.
repository: firecrawl/pdf-inspector
label: Testing
language: Rust
comments_count: 2
repository_stars: 13696
---

When tests target a particular guard, ordering, or threshold, ensure the test inputs actually exercise that exact logic (and not an earlier rejection/acceptance). Also pin threshold behavior with both sides.

How to apply:
- For layered predicates/gates, choose inputs that *pass all earlier gates* so the only reason the assertion holds/fails is the guard you intend to test.
- For boundary/threshold checks, add paired cases: one just outside (must fail) and one just inside (must pass). This prevents silent regressions where an unrelated condition starts handling the case.
- Make assertion messages consistent with reality: if the input is rejected earlier for a different reason, rename/replace it so the message matches the exercised behavior.

Example pattern (boundary + “caused-by” focus):
```rust
// Over-bound case: should fail only because it exceeds the bound
assert!(is_heading_fragment("IIIIIIIII. the value implies"));

// Within-bound case: should stay exempt when under/at the bound
assert!(!is_heading_fragment("IIIIIIII. What this implies"));
```

In practice: when a test feels “too easy” (or was introduced to protect a specific regression), double-check that the inputs reach the intended branch/guard and that each assertion would fail for the stated reason.