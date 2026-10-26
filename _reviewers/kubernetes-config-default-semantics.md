---
title: Config Default Semantics
description: When defining configuration API fields (including proto/API surface),
  make defaults and special values deterministic, consistent, and compatible with
  existing behavior.
repository: kUbernetes/kUbernetes
label: Configurations
language: Other
comments_count: 2
repository_stars: 128688
---

When defining configuration API fields (including proto/API surface), make defaults and special values deterministic, consistent, and compatible with existing behavior.

Apply this rule:
1) For optional fields (e.g., when a struct is nil), explicitly specify the exact assumed behavior and ensure it matches current runtime/system semantics for backward compatibility.
2) Avoid overloading sentinel values (like `-1`) with different meanings across subfields/types. Prefer uniform semantics; if a system cannot support the “unlimited” meaning directly, translate or clamp deterministically and enforce the policy at the API boundary via validation.
3) Ensure the chosen semantics are discoverable: update API comments and add validation logic/tests so users see failures or normalization behavior consistently.

Example (pattern):
```proto
// If the field is unset (nil), assume the compatibility mode.
// This must match existing runtime behavior.
optional CgroupnsOptions cgroupns_options = ...;
```
```go
// In API validation/normalization: make sentinel behavior uniform.
// If "-1" means "unlimited" for all ulimits, enforce via validation
// and deterministic clamping/translation for the one type that differs.
func validateUlimit(u Ulimit) error {
  // Reject duplicates, validate ranges, and handle "-1" uniformly.
}
```

Result: fewer surprising configuration differences across versions/runtimes, and less confusion for users configuring “special” values.