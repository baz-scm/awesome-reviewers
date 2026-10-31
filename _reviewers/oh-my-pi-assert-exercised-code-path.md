---
title: Assert exercised code path
description: When a test's behavior depends on an environment-specific or conditional
  code path (e.g., a feature that may silently fall back to an alternate implementation),
  guard the environment check separately from the assertion that the intended path
  actually ran. Never let a test pass simply because the conditional guard was false
  or because the fallback occurred —...
repository: can1357/oh-my-pi
label: Testing
language: Rust
comments_count: 3
repository_stars: 37317
---

When a test's behavior depends on an environment-specific or conditional code path (e.g., a feature that may silently fall back to an alternate implementation), guard the environment check separately from the assertion that the intended path actually ran. Never let a test pass simply because the conditional guard was false or because the fallback occurred — add an explicit assertion that the code path under test actually executed (e.g., `assert!(result.cloned_with.is_some())`) rather than only wrapping the real assertion in `if feature_available { ... }` or `if result.took_expected_path() { ... }`. A test that silently skips or no-ops when the implementation regresses provides false confidence and hides breakage.

Example of the problem:
```rust
// Bad: passes even if clone silently fell back to a plain checkout
let clone_works = clone_works_on(temp.path());
if clone_works {
    let result = repo.worktree_add(&dest, "target", opts);
    assert!(result.is_err()); // never true if fallback succeeds
}
```

Example of the fix:
```rust
let clone_works = clone_works_on(temp.path());
if clone_works {
    let result = repo.worktree_add(&dest, "target", opts).unwrap();
    // Explicitly assert the clone path was taken, not just that the call succeeded.
    assert!(result.cloned_with.is_some(), "expected clone, got fallback checkout");
}
```

Before merging a new test, confirm it is RED without the fix and GREEN with it (temporarily revert the fix and run the test to verify failure). This is the strongest evidence that the test actually covers the behavior it claims to, rather than trivially passing regardless of correctness.