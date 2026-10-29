---
title: Semantic accuracy in naming
description: Names must precisely describe what a variable, parameter, or function
  actually represents or does, not a narrower, vaguer, or purely mechanical description
  of it. Before naming, ask what the value or check means in the domain, then pick
  a name that reads correctly wherever it is used.
repository: cline/cline#1
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 71024
---

Names must precisely describe what a variable, parameter, or function actually represents or does, not a narrower, vaguer, or purely mechanical description of it. Before naming, ask what the value or check means in the domain, then pick a name that reads correctly wherever it is used.

Concretely:
- If a variable's computed value covers more cases than an old name implied (e.g. a readiness check that also accounts for turns still being prepared), rename it so the code reads as the test it actually performs (e.g. `canStartRun` → `sessionIdle`), rather than leaving a name that describes a stale or narrower concept.
- Avoid vague boolean parameters/flags whose meaning only becomes clear through negation or usage (e.g. a `background` flag that is always read as `!background`). Name it after the real-world condition it represents, such as `userInitiated`.
- When a field's domain has more than one meaningful state, prefer a descriptive string/enum over a boolean, since booleans force an awkward "not X" framing for the false case. For example, instead of `promptSeeded?: boolean`, model it as `source: "seeded" | "written"` so each state is named positively.
- Name functions so they read naturally at the call site, especially for async APIs (`await turnAccepted` reads better than `await whenTurnAccepted()`).
- When multiple exported functions or types serve overlapping purposes, don't leave callers to guess which one is correct from similar names (e.g. `findUsableFallbackProviderId` vs `resolveEffectiveLastUsedProviderId`). Either consolidate to a single, clearly-named entry point, or give each a name and doc comment that unambiguously signals when to use it.
- Keep related type names consistent across the codebase (e.g. a single shared `ClientName` type) rather than introducing parallel, divergent naming for the same concept.

Applying this standard means every identifier should let a reader predict its behavior or meaning without needing to trace through the implementation.