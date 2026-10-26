---
title: Semantic Identifier Naming
description: Use names that precisely describe the thing’s real semantics, and ensure
  the identifier is valid/unique within its naming “domain” (API fields, tests, labels).
repository: kUbernetes/kUbernetes
label: Naming Conventions
language: Go
comments_count: 8
repository_stars: 128688
---

Use names that precisely describe the thing’s real semantics, and ensure the identifier is valid/unique within its naming “domain” (API fields, tests, labels).

Practical rules:
- Match semantics: if a variable/function no longer represents what its name claims, rename it (don’t paper over with comments). Prefer names like `currentlyAllocatedCPUs` over `reusableCPUs` when it’s the current allocated CPUSet.
- Avoid misleading or “negative” API names when a clear positive alternative exists.
- Follow established test/label naming conventions, and make names unique where the framework requires it (e.g., `DescribeTable`/`Entry` full test name uniqueness).
- Don’t introduce confusing “almost the same” identifiers (e.g., two functions that differ only by case). Unify or rename to convey intent.
- When naming/matching depends on qualification or case sensitivity, don’t normalize silently; document the matching behavior and ensure names/fields reflect it.

Example (semantic rename):
```go
// Wrong: suggests a pool of allocatable CPUs, but this is the currently allocated CPUSet.
func newCPUAccumulatorForResize(..., reusableCPUs *cpuset.CPUSet, ...) { ... }

// Prefer:
func newCPUAccumulatorForResize(..., currentlyAllocatedCPUs *cpuset.CPUSet, ...) { ... }
```

Example (test name uniqueness):
- Ensure each `ginkgo.Entry("<unique description>", ...)` has a distinct description, because the framework builds a full test name from hierarchy + entry description.