---
title: Single Source Configuration
description: 'When configuration affects behavior (URLs, enablement flags, provider
  selection, session/bootstrap signals, or onboarding readiness), treat it as a single
  source of truth: resolve it once using shared contracts/helpers, pass the resolved
  value through, and never let separate components maintain divergent copies.'
repository: cline/cline#v3
label: Configurations
language: TypeScript
comments_count: 9
repository_stars: 70863
---

When configuration affects behavior (URLs, enablement flags, provider selection, session/bootstrap signals, or onboarding readiness), treat it as a single source of truth: resolve it once using shared contracts/helpers, pass the resolved value through, and never let separate components maintain divergent copies.

Apply this checklist:
- **Use shared resolution/parsing helpers** for anything derived from config/provider metadata (don’t re-implement frontmatter enablement, env key detection, base-url mapping, etc.).
- **Resolve at the correct lifecycle boundary** (e.g., at startup for host/app URLs) and pass the resolved value to downstream UI/webviews instead of recomputing per refresh/provider/account change.
- **Make precedence explicit** between CLI flags and environment variables—especially for negatable flags where defaults can silently override env fallback.
- **Treat resolved config as immutable** when passing to other subsystems; instrumentation/telemetry should attach data via hooks, not rewrite bootstrap truth fields (like session identifiers).
- **Isolate env for tests/smoke runs**: set explicit temp HOME/data/discovery/config dirs so parent environment cannot change outcomes.

Example (startup resolve + precedence-safe CLI/env):
```ts
// Resolve once from the backend/config mapping helper and pass down.
const apiBaseUrl = resolveBackendFromEnvOrConfig();
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // shared helper
ctx.clineAppBaseUrl = appBaseUrl; // immutable after startup

// CLI/env precedence with negatable flags (avoid commander default clobbering env).
const mouse =
  (authCmd.getOptionValueSource("mouse") === "cli"
    ? authCmd.opts().mouse
    : undefined) ??
  (program.getOptionValueSource("mouse") === "cli"
    ? program.opts().mouse
    : undefined) ??
  (process.env.CLINE_MOUSE !== "0" && process.env.CLINE_NO_MOUSE !== "1");
```

Result: fewer staging/production mismatches, no drifting UI logic vs core SDK rules, consistent provider readiness, and predictable behavior under varied env/CLI inputs.