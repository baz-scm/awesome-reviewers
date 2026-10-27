---
title: Config Schema And Modes
description: 'Ensure configuration-driven behavior is both correct and predictable:


  1) Use documented config/rule schema keys exactly

  - If a config file supports path-scoped rules, use the documented key (e.g., prefer
  `paths:` over `globs:` when that’s what the tooling expects), otherwise the intended
  rules may silently not apply.'
repository: facebook/react#b12
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 251896
---

Ensure configuration-driven behavior is both correct and predictable:

1) Use documented config/rule schema keys exactly
- If a config file supports path-scoped rules, use the documented key (e.g., prefer `paths:` over `globs:` when that’s what the tooling expects), otherwise the intended rules may silently not apply.

2) Separate validation intent with feature flags
- When the system has different goals (e.g., “compiler correctness” vs “linting precision”), add an explicit feature flag for the mode.
- Define acceptance criteria per mode:
  - Compiler mode: allow “correct enough” deps (e.g., `[x]` covers `x`-derived reads even if more-specific subsources exist).
  - Lint mode: require the most precise deps and treat unnecessary/less-precise deps as errors (e.g., error on `[x, x.y]` and suggest `[x]`).

3) Make fixes actionable with location-aware diagnostics
- Track and emit source locations for both the inferred deps and the manual deps array literal so suggestions can point to the exact code to replace.

Example (mode split concept):
```ts
// pseudo
if (mode === 'compiler') {
  // validate deps are correct; be permissive about extra specificity
} else if (mode === 'lint') {
  // validate deps are maximally precise; reject unnecessary deps
}
// diagnostics should include locations for manual deps array literals
```