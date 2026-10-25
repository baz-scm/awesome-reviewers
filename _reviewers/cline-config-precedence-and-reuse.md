---
title: Config precedence and reuse
description: 'Implement configuration resolution with deterministic precedence and
  reuse resolved values instead of re-deriving them in multiple places.


  **Standards**'
repository: ClInE/cLiNe
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70838
---

Implement configuration resolution with deterministic precedence and reuse resolved values instead of re-deriving them in multiple places.

**Standards**
1. **Explicit wins:** If an option/flag is explicitly provided, it must override any derived/default value.
   - Example pattern: `allowBindFallback: userProvided ?? derivedDefault`.
2. **CLI/env precedence must respect “source”:** For CLI libraries that default negatable flags, don’t read the raw option value to decide whether the user intended a change. Use the option’s source to avoid clobbering env fallbacks.
3. **Single-source mapping:** When you resolve one base/config value (e.g., backend/API base URL), derive dependent values (e.g., app/web link base URL) from that same resolved result via a shared helper—don’t re-resolve from a different config key.
4. **Resolve once at startup when assumptions are stable:** If the app/backend/environment won’t change during runtime, resolve provider/env-derived values once during context creation, store them (e.g., `ctx.clineAppBaseUrl`), and serve them without re-reading provider settings on each request.
5. **Unify selection rules across layers:** If two components select the “primary” remote/provider item, ensure they use the same rule/helper; divergent rules can cause mismatched targets.

**Illustrative snippets**
```ts
// 1) Explicit option wins
const allowBindFallback = explicitAllowBindFallback ?? !hasExplicitEndpoint;

// 2) CLI vs env: only use CLI value when it was actually set on CLI
const mouse =
  cmd.getOptionValueSource('mouse') === 'cli' ? cmd.opts().mouse : undefined;
const useMouse =
  input.mouse !== undefined ? input.mouse : process.env.CLINE_MOUSE !== '0';

// 3) Single-source mapping: resolve backend once, map to app URL from it
const apiBaseUrl = resolveBackendApiBaseUrl();
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // shared helper

// 4) Resolve once and reuse (sidecar/webview)
ctx.clineAppBaseUrl = appBaseUrl;
function get_cline_app_base_url() { return ctx.clineAppBaseUrl; }
```

Following these rules prevents the common class of bugs where the UI/link targets one environment while the backend call uses another, where env fallbacks are silently overridden by CLI defaults, or where explicit runtime options are ignored due to derived defaults.