---
title: Deterministic config precedence
description: 'Ensure configuration resolution is deterministic, consistent across
  components, and respects explicit precedence rules.


  Apply this when adding/changing env vars, flags, config-file parsing, or derived
  URLs/actions.'
repository: cline/cline#v5
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Ensure configuration resolution is deterministic, consistent across components, and respects explicit precedence rules.

Apply this when adding/changing env vars, flags, config-file parsing, or derived URLs/actions.

**Rules**
1. **Single source of truth:** Reuse shared helpers/SDK parsing instead of duplicating enable/disable or parsing rules.
2. **Resolve once per supported lifecycle:** If the app can’t switch backends/environments after startup, resolve those values once and pass them through (don’t recompute on every refresh).
3. **Precedence is explicit and correct:** Use “caller/CLI override wins” semantics over derived defaults and avoid library defaulting clobbering env fallback.
4. **Use the same resolved base everywhere:** If you resolve a backend/base URL with provider overrides, build any environment-specific links/actions from that exact resolved value (and hide actions when no valid mapping exists).
5. **Tests run under hostile isolation:** Smoke/regression tests should override discovery/data paths to avoid touching real user services.

**Example patterns**

CLI flag/env precedence (avoid Commander negatable defaults clobbering env):
```ts
const flagProvided = cmd.getOptionValueSource("mouse") === "cli";
const mouse = flagProvided ? cmd.opts().mouse : undefined;
const resolved = mouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

Resolve once and pass through:
```ts
// startup resolution
const appBaseUrl = resolveClineAppBaseUrl(resolvedApiBaseUrl);
ctx.clineAppBaseUrl = appBaseUrl;

// sidecar command just returns the resolved value
if (command === "get_cline_app_base_url") return ctx.clineAppBaseUrl;
```

By following these, you prevent environment/link mismatches, config parser drift, and subtle precedence bugs across CLI, desktop/webview, and runtime components.