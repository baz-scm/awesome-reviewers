---
title: Enforce Layered Reuse
description: 'When changing or adding code, keep logic and dependencies clean:


  - Centralize invariants in the owning function: if you need to clamp/validate values,
  apply it inside the core method that produces/returns them (the “source of truth”)
  rather than at every call site.'
repository: looplj/axonhub
label: Code Style
language: Go
comments_count: 3
repository_stars: 4808
---

When changing or adding code, keep logic and dependencies clean:

- Centralize invariants in the owning function: if you need to clamp/validate values, apply it inside the core method that produces/returns them (the “source of truth”) rather than at every call site.
- Respect package layering: lower-level packages must not import higher-level/business packages (no reverse dependencies). Define contracts in the appropriate layer so dependencies flow downward only.
- Reuse existing utilities: avoid adding tiny wrappers/helpers when an approved library/helper already exists.

Example (centralize clamping):
```go
// prefer: clamp inside Calculate (source of truth)
first, request, _ := ts.perf.Calculate() // already returns clamped request
```

Example (no reverse dependency):
- If `llm` is a bottom package, it should not `import objects` (business). Move shared types to a neutral/lower package or pass data via interfaces defined at the lower layer.

Example (reuse utility):
```go
v := lo.ToPtr(123) // instead of custom xptr.IntPtr(123)
```