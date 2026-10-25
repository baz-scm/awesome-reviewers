---
title: Consistent Configuration Resolution
description: Configuration-derived behavior must be resolved in one authoritative
  phase (startup or request construction) and then passed through without recomputation
  or semantic mutation. Divergence (different resolution rules for UI vs runtime,
  per-refresh re-reads, or observer code changing core inputs) causes environment
  mismatches, wrong URLs/remotes, and...
repository: CLINE/CLINE
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70837
---

Configuration-derived behavior must be resolved in one authoritative phase (startup or request construction) and then passed through without recomputation or semantic mutation. Divergence (different resolution rules for UI vs runtime, per-refresh re-reads, or observer code changing core inputs) causes environment mismatches, wrong URLs/remotes, and incorrect session semantics.

Apply these rules:
1) Use shared helpers for derived config decisions (URLs, env-var meaning, parsing rules). Don’t rebuild values from different config roots.
2) Resolve once, reuse everywhere. If switching providers/backends/environments is not supported after startup, do not re-resolve on each refresh/account load.
3) Treat bootstrap/config fields as immutable semantics for core. Features like telemetry must not mutate fields that change core interpretation (e.g., `sessionId`, restart signals).
4) Keep tests/smoke probes isolated by overriding config discovery paths and data dirs so they can’t read/write real user state.

Example pattern (resolve once, don’t mutate core):
```ts
// startup (authoritative resolution)
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl);
ctx.clineAppBaseUrl = appBaseUrl; // pass-through, not recomputed later

// request/command handler
if (command === "get_cline_app_base_url") {
  return ctx.clineAppBaseUrl; // reuse resolved value
}

// telemetry: attach hooks; do not rewrite semantic config
const coreInput = { ...inputWithRemoteConfig.config, /* no changes to sessionId */ };
coreInput.hooks = { ...coreInput.hooks, ...telemetryHooks };
return coreInput;
```

This standard prevents repo/URL mismatches, staging/prod link errors, env-key onboarding drift, and “observer” side effects that change core behavior.