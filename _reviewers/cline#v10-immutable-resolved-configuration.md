---
title: Immutable, Resolved Configuration
description: When configuration affects behavior, treat it as (a) resolved once from
  the correct sources, (b) shared via common helpers to avoid semantic drift, and
  (c) immutable from observer-like layers.
repository: cline/cline#v10
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70869
---

When configuration affects behavior, treat it as (a) resolved once from the correct sources, (b) shared via common helpers to avoid semantic drift, and (c) immutable from observer-like layers.

Apply these rules:
- Resolve environment-specific values once (e.g., app base URLs) during startup/config resolution, then pass the resolved value downstream; avoid re-resolving on every refresh if the backend/environment cannot change.
- Centralize the semantics of “what a config means” (parsing rules, enable/disable precedence, provider eligibility, URL mapping). Don’t maintain parallel copies in different packages—reuse the shared SDK/runtime helpers.
- Make precedence explicit: if both CLI flags and env vars exist, resolve based on the *source* of the option (e.g., detect whether Commander populated it from CLI vs default negation) so defaults don’t overwrite env fallback.
- Don’t let telemetry/observers mutate bootstrap config that core uses for state interpretation. Prefer returning hook wiring while keeping the original core input shape (especially fields whose presence/absence changes behavior).
- In build/test, isolate configuration paths and ports in a temporary HOME/data directory so discovery mechanisms don’t touch real developer state.

Example pattern:
```ts
// 1) Resolve once
const resolvedAppBaseUrl = resolveClineAppBaseUrl(resolvedBackendBaseUrl);
ctx.clineAppBaseUrl = resolvedAppBaseUrl; // pass-through, not recomputed per refresh

// 2) Build behavior without mutating bootstrap truth
function configureCore(input: CoreStartInput, telemetry: TelemetryOptions) {
  const hooks = makeTelemetryHooks(telemetry);
  // Keep bootstrap config untouched: core sees the same input it would otherwise
  return { ...input, hooks };
}

// 3) Explicit precedence for negatable flags
const mouse =
  (authCmd.getOptionValueSource('mouse') === 'cli' ? authCmd.opts().mouse : undefined) ??
  (program.getOptionValueSource('mouse') === 'cli' ? program.opts().mouse : undefined);

const useMouse = mouse !== undefined ? mouse : envFallback();
```

If you follow this checklist, you prevent the common failure modes shown here: environment mismatches, drift between duplicated parsing/eligibility logic, env/CLI precedence bugs, and observer-induced state changes.