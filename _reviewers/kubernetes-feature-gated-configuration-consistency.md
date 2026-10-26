---
title: Feature-gated Configuration Consistency
description: When adding or changing a feature-gated configuration/behavior, ensure
  the gate is applied consistently across *all* layers (API defaults/validation, admission
  checks, and runtime logic), and that turning the gate off preserves the previous/legacy
  behavior (including how updates treat existing stored fields/status).
repository: kUbernetes/kUbernetes
label: Configurations
language: Go
comments_count: 13
repository_stars: 128688
---

When adding or changing a feature-gated configuration/behavior, ensure the gate is applied consistently across *all* layers (API defaults/validation, admission checks, and runtime logic), and that turning the gate off preserves the previous/legacy behavior (including how updates treat existing stored fields/status).

Practical rules:
1) Gate everywhere the behavior is relevant
- If a new field/behavior is guarded by a feature gate, do not rely on defaults or “declarative validation” to enforce it.
- Apply the gate in API validation and (if applicable) admission, and short-circuit runtime code paths when the gate is disabled.

2) Gate-off must be a true no-op (no CycleState writes, no allocation/validation side effects)
- Avoid executing new logic when the feature is off. Prefer early returns / disabled plugin registration.

3) Preserve existing data when the gate is disabled
- For update/merge logic, include explicit test cases for:
  - keep when enabled
  - drop when disabled
  - keep when objects already contain the fields/status but updates don’t change them

4) Keep feature gate names/versions/dependencies accurate
- Ensure gate definitions and dependencies match the Kubernetes versions used in CI/tests (avoid “unknown feature gate” errors).

Example pattern (consistent short-circuit):
```go
func (p *something) applyOnResize(...) error {
  if !utilfeature.DefaultFeatureGate.Enabled(features.InPlacePodVerticalScaling) ||
     !utilfeature.DefaultFeatureGate.Enabled(features.InPlacePodVerticalScalingExclusiveCPUs) {
    logger.V(2).Info("skipped resize allocation: feature gates disabled")
    return nil // gate-off must not change state
  }

  // additional checks driven by resource semantics (e.g., pod-level vs container-level)
  // ...
  return nil
}
```

Add/extend unit/integration tests to cover enable/disable and preserve-existing scenarios, not just the enabled path.