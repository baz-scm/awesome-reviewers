---
title: Behavioral Regression Tests
description: Write regression tests that (1) are portable across platforms where behavior
  is shared and (2) are “behaviorally decisive,” meaning they must fail if the real
  logic is removed.
repository: ogulcancelik/herdr
label: Testing
language: Rust
comments_count: 2
repository_stars: 26924
---

Write regression tests that (1) are portable across platforms where behavior is shared and (2) are “behaviorally decisive,” meaning they must fail if the real logic is removed.

Apply:
- Use broad `cfg` gates for shared behavior (e.g., `#[cfg(unix)]`) rather than narrow OS-specific gates in core modules.
- Shape fixtures so the expected state transition is not satisfied by index coincidences or incidental setup. If your code must “reconcile” selection/focus after deletion or shifting, pick a scenario where indices change and the reconciliation block is required.

Example (portability + decisive setup):
```rust
#[cfg(unix)]
#[test]
fn preserves_selection_after_close_requiring_reconciliation() {
    // Arrange: 3 workspaces so the survivor index shifts
    // e.g., [background (only tab), middle, active (selected)]

    // Act: close background's last tab

    // Assert: selected workspace is updated by reconciliation logic,
    // and the test would fail if focus/selection reconciliation were removed.
}
```

This standard prevents flaky/overly restrictive platform gating and ensures regression tests actually guard the behavior you care about.