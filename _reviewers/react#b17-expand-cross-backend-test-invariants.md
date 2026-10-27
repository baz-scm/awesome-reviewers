---
title: Expand cross-backend test invariants
description: Add test coverage that (1) validates critical invariants across the *entire*
  produced output for *all* backends, (2) includes targeted fixtures for edge-case
  semantics when protections are loosened/removed, and (3) keeps E2E tests deterministic
  and state-aware.
repository: facebook/react#b17
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251891
---

Add test coverage that (1) validates critical invariants across the *entire* produced output for *all* backends, (2) includes targeted fixtures for edge-case semantics when protections are loosened/removed, and (3) keeps E2E tests deterministic and state-aware.

How to apply:
- Global harness assertions: prefer checking invariants for every relevant output node, not only declaration subsets. When you have range metadata, validate index alignment and ordering for all nodes that carry the necessary fields.
- Targeted compilation/type fixtures: if a change could alter how method/property calls are emitted or typed, construct a minimal example that matches the risky shape (e.g., receiver semantics + return type) and verify it compiles/behaves as expected.
- Deterministic E2E selection + state coverage: avoid brittle positional selectors (`nth(...)`). Use `data-testid` for tab/panel selection and add a test that runs the UI in both important modes (e.g., internals shown vs hidden).

Example (global range invariant check idea):
```ts
// In the shared snapshot/harness where you traverse the full output AST
for (const node of outputAstNodes) {
  if (
    typeof node.start === 'number' &&
    typeof node.end === 'number' &&
    node.loc?.index != null
  ) {
    // start/end must align to the same index space as loc
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
```

Outcome: regressions are caught early (via invariant checks + semantic fixtures) and end-to-end suites remain stable (via test IDs and explicit UI state toggles).