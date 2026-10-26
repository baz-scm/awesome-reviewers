---
title: Single-Source Configuration Resolution
description: When code depends on configuration (env vars, provider baseUrl, feature
  flags, parsed metadata), treat configuration resolution as a deterministic, single-source
  operation.
repository: cline/cline?x=1
label: Configurations
language: TypeScript
comments_count: 9
repository_stars: 70861
---

When code depends on configuration (env vars, provider baseUrl, feature flags, parsed metadata), treat configuration resolution as a deterministic, single-source operation.

Apply these rules:
1) Resolve once, at startup (or at the exact boundary where inputs are known), and pass the resolved values through. Don’t re-read/rehydrate provider settings in refresh/account-refresh paths.
2) Derive all dependent decisions (links, UI labels, gating, behavior targets) from the same resolved value; don’t let one subsystem use a different baseUrl/remote/semantics.
3) Reuse shared helpers for parsing and eligibility checks (e.g., YAML enable/disable rules, “is this env var actually an API key?”) instead of duplicating logic.
4) Make precedence explicit and guard against silent clobbering (e.g., Commander negatable flags defaulting a value). Resolve precedence based on value source, not only raw option values.
5) Treat “bootstrap truth” config passed to other layers as immutable. Don’t mutate input-derived config to add telemetry/session fields that can change downstream behavior semantics.

Example (env/flag precedence guard):
```ts
// Prefer CLI only when the option was explicitly supplied; otherwise fall back to env.
const mouse =
  (authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
  (program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined) ??
  (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

Example (compute once and pass down):
```ts
// During startup resolution:
const appBaseUrl = resolveClineAppBaseUrl(resolvedApiBaseUrl);
ctx.appBaseUrl = appBaseUrl;

// Later handler just returns the already-resolved field.
return ctx.appBaseUrl; 
```