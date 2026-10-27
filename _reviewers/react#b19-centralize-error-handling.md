---
title: Centralize error handling
description: Errors and invariant failures must be raised with accurate, context-aware
  messages and surfaced through a single, well-defined handling point rather than
  thrown ad hoc or silently swallowed. When adding a new validation/analysis pass,
  don't throw errors directly from deep within the pass; instead return/collect them
  and let the top-level entry point (e.g....
repository: facebook/react#b19
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 251893
---

Errors and invariant failures must be raised with accurate, context-aware messages and surfaced through a single, well-defined handling point rather than thrown ad hoc or silently swallowed. When adding a new validation/analysis pass, don't throw errors directly from deep within the pass; instead return/collect them and let the top-level entry point (e.g. the pipeline's `run` function) decide whether to log or throw, so error handling stays consistent across passes. When writing invariant checks that cover multiple cases, make the message reflect the actual case that failed instead of hardcoding one variant:

```ts
// Bad: message doesn't reflect which effect kind actually failed
CompilerError.invariant(
  effect.kind === 'Capture' || effect.kind === 'MaybeAlias' || initialized.has(...),
  { reason: `Expected destination value to already be initialized ... for Alias effect` }
);

// Good: message is derived from the actual effect
CompilerError.invariant(
  effect.kind === 'Capture' || effect.kind === 'MaybeAlias' || initialized.has(...),
  { reason: `Expected destination value to already be initialized ... for ${effect.kind} effect` }
);
```

Finally, verify that failure paths are actually observable by users: an invariant or internal error that never gets reported (e.g. because it isn't wired into eslint diagnostics) effectively becomes a silent failure, such as missing shape definitions causing property-resolution errors that users never see. Always add tests or checks confirming that error paths you introduce are reachable and reported through the standard diagnostic/error-reporting channel.