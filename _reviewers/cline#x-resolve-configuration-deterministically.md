---
title: Resolve configuration deterministically
description: When behavior depends on derived configuration (remote selection, app/backend
  base URLs, feature flags, etc.), resolve that configuration deterministically once
  from the final environment/config inputs, then reuse the exact resolved values everywhere.
repository: cline/cline#x
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70861
---

When behavior depends on derived configuration (remote selection, app/backend base URLs, feature flags, etc.), resolve that configuration deterministically once from the final environment/config inputs, then reuse the exact resolved values everywhere.

Apply this standard:
- **Single source of truth:** Use the same mapping helper for “provider/backend → environment/app URL” (and similar conversions) rather than assembling links/decisions from different fields.
- **Resolve once at startup when runtime can’t change:** If the app doesn’t support switching accounts/backends/environments after startup, compute the resolved values during startup (or context creation) and pass them through. Avoid re-resolving on refresh flows.
- **Unify selection rules:** If one rule decides what will be pushed to (e.g., git remote choice) and another rule decides what to display, make them identical by reusing the same selection logic.
- **Be explicit about config precedence:** For CLI flags + env fallbacks, ensure negatable/default CLI values don’t clobber env. Prefer checking the **value source** (e.g., only use the option when it was actually provided).
- **Isolate env roots in tests/smoke runs:** When testing under env/config, set all relevant root variables (HOME/data/discovery paths/ports) inside the temp directory so parent env can’t leak.

Example (value-source precedence to avoid negatable flag clobbering env):
```ts
const cliProvidedMouse = program.getOptionValueSource("mouse") === "cli";
const mouse = cliProvidedMouse ? program.opts().mouse : undefined;
const useMouse = mouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

Example (resolve once and reuse a concrete app base URL):
```ts
// startup/context creation
const apiBaseUrl = resolveAccountApiBaseUrl(/* resolved config */);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // may be undefined
ctx.clineAppBaseUrl = appBaseUrl;

// later, in webview/sidecar command
if (command === "get_cline_app_base_url") return ctx.clineAppBaseUrl;
```